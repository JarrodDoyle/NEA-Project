from map_generation.dungeon_base import Dungeon
import random, cells
from floodfill import flood_fill
from entities.entity_functions import get_blocking_entity

class Dungeon_Cellular_Automata(Dungeon):
    def __init__(self, width, height, birth_limit, death_limit, chance_to_be_alive, num_steps):
        super().__init__(width - 2, height - 2)
        self.set_ruleset(birth_limit, death_limit, chance_to_be_alive)
        self.num_steps = num_steps

    def initialize_dungeon(self):
        self.tiles = [[cells.Rock() for x in range(self.width)]for y in range(self.height)]
        self.room_arr = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if random.randint(0, 100) <= self.chance_to_be_alive:
                    row.append(1)
                else:
                    row.append(0)
            self.room_arr.append(row)

        # Doesn't take chance to be alive into account
        # self.tiles = [[[1, 0][random.randint(0,100) < self.chance_to_be_alive] for x in range(self.width)] for y in range(self.height)]

    def simulate_step(self):
        new_tiles = self.room_arr
        for y in range(self.height):
            for x in range(self.width):
                num_alive = self.check_neighbourhood((x, y))
                if self.room_arr[y][x]:
                    if num_alive < self.death_limit:
                        new_tiles[y][x] = 0
                if not self.room_arr[y][x]:
                    if num_alive > self.birth_limit:
                        new_tiles[y][x] = 1
        self.room_arr = new_tiles

    def check_neighbourhood(self, cell_coords):
        cell_x, cell_y = cell_coords
        cell = self.room_arr[cell_y][cell_x]
        alive = 0
        dead = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx != 0 or dy != 0:
                    x = cell_x + dx
                    y = cell_y + dy
                    if x in range(0, self.width) and y in range(0, self.height):
                        neighbour = self.room_arr[y][x]
                        alive += neighbour
                    # Consider out of bounds neighbours as alive
                    else:
                        alive += 1
        return alive

    def set_ruleset(self, birth_limit, death_limit, chance_to_be_alive):
        self.birth_limit = birth_limit
        self.death_limit = death_limit
        self.chance_to_be_alive = chance_to_be_alive

    def connect_rooms(self):
        base_mark = 0
        room_mark = 2
        rooms_calculated = False
        while not rooms_calculated:
            rooms_calculated = True
            for y in range(self.height):
                for x in range(self.width):
                    cell = self.room_arr[y][x]
                    if cell == 0:
                        flood_fill(self.room_arr, (x, y), base_mark, room_mark)
                        room_mark += 1
                        rooms_calculated = False
        room_count = room_mark - 1
        for i in range(room_count):
            if i + 2 < room_mark - 1:
                p1 = None
                p2 = None
                for y in range(self.height):
                    for x in range(self.width):
                        if self.room_arr[y][x] == i + 2:
                            p1 = [x, y]
                            break
                    if p1 != None:
                        break
                for y in range(self.height):
                    for x in range(self.width):
                        if self.room_arr[y][x] == i + 3:
                            p2 = [x, y]
                            break
                    if p2 != None:
                        break
                self.dig_corridor(p1, p2)

    def convert_dungeon(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.room_arr[y][x] != 1:
                    self.tiles[y][x] = cells.Floor()

    def dig_v_corridor(self, x, y1, y2):
        for y in range(y1, y2 + 1):
            self.tiles[y][x] = cells.Floor()

    def dig_h_corridor(self, y, x1, x2):
        for x in range(x1, x2 + 1):
            self.tiles[y][x] = cells.Floor()

    def dig_corridor(self, p1, p2):
        x1 = min(p1[0], p2[0])
        x2 = max(p1[0], p2[0])
        y1 = min(p1[1], p2[1])
        y2 = max(p1[1], p2[1])

        if random.randint(0, 1):
            #dig h-v-h
            x3 = x2
            x2 = (x1 + x3) // 2
            if p1[0] > p2[0]:
                self.dig_h_corridor(y1, x2, x3)
                self.dig_v_corridor(x2, y1, y2)
                self.dig_h_corridor(y2, x1, x2)
            else:
                self.dig_h_corridor(y1, x1, x2)
                self.dig_v_corridor(x2, y1, y2)
                self.dig_h_corridor(y2, x2, x3)
        else:
            #dig v-h-v
            y3 = y2
            y2 = (y1 + y3) // 2
            if p1[0] > p2[0]:
                self.dig_v_corridor(x1, y2, y3)
                self.dig_h_corridor(y2, x1, x2)
                self.dig_v_corridor(x2, y1, y2)
            else:
                self.dig_v_corridor(x1, y1, y2)
                self.dig_h_corridor(y2, x1, x2)
                self.dig_v_corridor(x2, y2, y3)

    def gen_dungeon(self, player):
        self.initialize_dungeon()
        for i in range(self.num_steps):
            self.simulate_step()
        self.connect_rooms()
        self.convert_dungeon()
        self.set_player_coords(player, rooms = False)
        entity_list = [player]
        self.gen_stairs()
        self.gen_monsters(player, entity_list)
        self.gen_items(entity_list)

        # Insert border around dungeon
        self.tiles.insert(0, [cells.Rock() for x in range(self.width)])
        self.tiles.append([cells.Rock() for x in range(self.width)])
        for y in self.tiles:
            y.insert(0, cells.Rock())
            y.append(cells.Rock())
        self.width += 2
        self.height += 2

        # Adjust entity coordinates
        for entity in entity_list:
            entity.x += 1
            entity.y += 1
        return entity_list
