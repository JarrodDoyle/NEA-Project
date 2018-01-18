from map_generation.dungeon_base import Dungeon
from rect import Rect
from kruskals import Kruskals_Algorithm
import random, cells

class Dungeon_Mazes_And_Rooms(Dungeon):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.initialize_dungeon(tile = 0)

    def gen_rooms(self, attempts):
        '''Make a specified number of attempts to generate rooms'''
        self.rooms = []
        for i in range(attempts):
            x = random.choice([i for i in range(1, self.width, 2)])
            y = random.choice([i for i in range(1, self.height, 2)])
            rect = self.gen_rand_odd_rect(x, y, 5, 9) # 5 and 9 are min/max room size including walls
            valid_room = True
            for i in range(x, rect.x2 + 1):
                for j in range(y, rect.y2 + 1):
                    if i >= self.width or j >= self.height:
                        valid_room = False
                        break
                    elif self.tiles[j][i] is None:
                        valid_room = False
                        break
                if not valid_room:
                    break
            else:
                self.rooms.append(rect)
                for i in range(x, rect.x2 + 1):
                    for j in range(y, rect.y2 + 1):
                        self.tiles[j][i] = None

    def build_floors(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.tiles[y][x] != None:
                    self.tiles[y][x] = cells.Floor()

    def build_walls(self):
        for room in self.rooms:
            for x in range(room.x1 - 1, room.x2 + 2):
                if self.tiles[room.y1 - 1][x].is_blocked:
                    self.tiles[room.y1 - 1][x] = cells.Wall()
                if self.tiles[room.y2 + 1][x].is_blocked:
                    self.tiles[room.y2 + 1][x] = cells.Wall()
            for y in range(room.y1 - 1, room.y2 + 2):
                if self.tiles[y][room.x1 - 1].is_blocked:
                    self.tiles[y][room.x1 - 1] = cells.Wall()
                if self.tiles[y][room.x2 + 1].is_blocked:
                    self.tiles[y][room.x2 + 1] = cells.Wall()

    def build_room_regions(self):
        '''Finds highest current region id and gives each room an id above it'''
        max_region_id = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.tiles[y][x] != None and self.tiles[y][x] > max_region_id:
                    max_region_id = self.tiles[y][x]
        room_region_id = max_region_id + 1
        for room in self.rooms:
            for y in range(room.y1, room.y2 + 1):
                for x in range(room.x1, room.x2 + 1):
                    self.tiles[y][x] = room_region_id
            room_region_id += 1

    def gen_mazes(self):
        '''Gen perfect mazes in empty areas using kruskals'''
        mazes = Kruskals_Algorithm(self.tiles)
        mazes.gen_maze()
        return mazes.arr

    def gen_connections(self):
        '''Find valid connection points between regions'''
        connections = []
        for y in range(self.height):
            for x in range(self.width):
                if 0 < x < self.width - 1 and 0 < y < self.height - 1 and self.tiles[y][x] == None:
                    above = self.tiles[y-1][x]
                    below = self.tiles[y+1][x]
                    left = self.tiles[y][x-1]
                    right = self.tiles[y][x+1]
                    if above != None and below != None and above != below:
                        connections.append([x, y, "v"])
                    elif left != None and right != None and left != right:
                        connections.append([x, y, "h"])
        return connections

    def remove_invalid_connections(self, connections):
        invalid_connections = []
        for connection in connections:
            x, y, direction = connection
            if self.tiles[y][x] != None:
                invalid_connections.append(connection)
            elif direction == "v":
                if self.tiles[y-1][x] == self.tiles[y+1][x]:
                    invalid_connections.append(connection)
            elif direction == "h":
                if self.tiles[y][x-1] == self.tiles[y][x+1]:
                    invalid_connections.append(connection)
        for connection in invalid_connections:
            connections.remove(connection)
        return connections, invalid_connections

    def make_connection(self, connection):
        x, y, direction = connection
        if direction == "v":
            id1 = self.tiles[y-1][x]
            id2 = self.tiles[y+1][x]
        elif direction == "h":
            id1 = self.tiles[y][x-1]
            id2 = self.tiles[y][x+1]
        self.tiles[y][x] = id1
        if id1 != id2:
            for y in range(self.height):
                for x in range(self.width):
                    if self.tiles[y][x] == id2:
                        self.tiles[y][x] = id1

    def connect_dungeon(self, connections):
        '''Adds at least one connection to the dungeon'''
        connection = random.choice(connections)
        self.make_connection(connection)
        connections, lost_connections = self.remove_invalid_connections(connections)
        for lost_connection in lost_connections:
            dx, dy = connection[0] - lost_connection[0], connection[1] - lost_connection[1]
            if [dx, dy] not in [[0,1],[1,0],[0,-1],[-1,0]] and not random.randint(0,50):
                self.make_connection(lost_connection)
        return connections

    def remove_dead_ends(self):
        '''iterate over mazes and remove dead ends'''
        done = False
        while not done:
            done = True
            for y in range(self.height):
                for x in range(self.width):
                    if self.tiles[y][x].cell_name == "floor":
                        exits = 0
                        for dx in [-1, 1]:
                            if 0 <= x + dx < self.width and self.tiles[y][x+dx].cell_name == "floor":
                                exits += 1
                        for dy in [-1, 1]:
                            if 0 <= y + dy < self.height and  self.tiles[y+dy][x].cell_name == "floor":
                                exits += 1
                        if exits == 1:
                            self.tiles[y][x] = cells.Rock()
                            done = False

    def fill_blank_space(self):
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                if self.tiles[y][x] is None:
                    self.tiles[y][x] = cells.Rock()

    def gen_rand_odd_rect(self, x, y, min_size, max_size):
        '''Generate a rect object with odd length sides.'''
        width = random.choice([i for i in range(min_size, max_size + 1, 2)])
        height = random.choice([i for i in range(min_size, max_size + 1, 2)])
        return Rect(x, y, width, height)

    def gen_dungeon(self, player, attempts):
        self.gen_rooms(attempts)
        self.tiles = self.gen_mazes()
        self.build_room_regions()
        connections = self.gen_connections()
        while len(connections) > 0:
            connections = self.connect_dungeon(connections)
        self.build_floors()
        self.fill_blank_space()
        self.build_walls()
        self.remove_dead_ends()

        self.set_player_coords(player)
        entity_list = [player]

        self.gen_monsters(player, entity_list, only_in_rooms = True)
        self.gen_items(entity_list, only_in_rooms = True)
        self.gen_stairs(only_in_rooms = True)
        return entity_list
