from map_generation.dungeon_base import Dungeon
import random, cells
from floodfill import flood_fill

class Dungeon_Cellular_Automata(Dungeon):
    def __init__(self, width, height, birth_limit, death_limit, chance_to_be_alive):
        super().__init__(width, height)
        self.set_ruleset(birth_limit, death_limit, chance_to_be_alive)
        
    def initialize_dungeon(self):
        self.tiles = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if random.randint(0, 100) <= self.chance_to_be_alive:
                    row.append(1)
                else:
                    row.append(0)
            self.tiles.append(row)

        # Doesn't take chance to be alive into account
        #self.tiles = [[[1, 0][random.randint(0,1)] for x in range(self.width)] for y in range(self.height)]

    def simulate_step(self):
        new_tiles = self.tiles
        for y in range(self.height):
            for x in range(self.width):
                num_alive = self.check_neighbourhood((x, y))
                if self.tiles[y][x]:
                    if num_alive < self.death_limit:
                        new_tiles[y][x] = 0
                if not self.tiles[y][x]:
                    if num_alive > self.birth_limit:
                        new_tiles[y][x] = 1
        self.tiles = new_tiles

    def check_neighbourhood(self, cell_coords):
        cell_x, cell_y = cell_coords
        cell = self.tiles[cell_y][cell_x]
        alive = 0
        dead = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx != 0 or dy != 0:
                    x = cell_x + dx
                    y = cell_y + dy
                    if x in range(0, self.width) and y in range(0, self.height):
                        neighbour = self.tiles[y][x]
                        alive += neighbour
                    # Consider out of bounds neighbours as alive
                    else:
                        alive += 1
        return alive

    def display_dungeon(self):
        for y in self.tiles:
            for x in y:
                print(x, end="")
            print()

    def set_ruleset(self, birth_limit, death_limit, chance_to_be_alive):
        self.birth_limit = birth_limit
        self.death_limit = death_limit
        self.chance_to_be_alive = chance_to_be_alive

    def check_connectivity(self):
        base_mark = 0
        room_mark = 2
        room_count = 0
        rooms_calculated = False
        while not rooms_calculated:
            rooms_calculated = True
            for y in range(self.height):
                for x in range(self.width):
                    cell = self.tiles[y][x]
                    if cell > room_count - 2:
                        room_count = cell - 2
                    if cell == 0:
                        flood_fill(self.tiles, (x, y), base_mark, room_mark)
                        room_mark += 1
                        rooms_calculated = False
                    
