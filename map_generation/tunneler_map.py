import libtcodpy as libtcod
import cells, random
from rect import Rect
from entities.entity_functions import get_blocking_entity
from entities.entity_classes import *

class Dungeon_Tunneler:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def initialize_dungeon(self):
        self.tiles = [[cells.Rock() for x in range(self.width)] for y in range(self.height)]

    def gen_room(self):
        width = libtcod.random_get_int(None, 4, 8)
        height = libtcod.random_get_int(None, 4, 8)
        x = libtcod.random_get_int(None, 0, self.width - 1 - width)
        y = libtcod.random_get_int(None, 0, self.height - 1 - height)

        valid_room = True
        for row in range(y, y + height + 1):
            for column in range(x, x + width + 1):
                if self.tiles[row][column].cell_name != "rock":
                    valid_room = False

        if valid_room:
            room = Rect(x, y, width, height)
            for row in range(y, y + height + 1):
                for column in  range(x, x + width + 1):
                    self.tiles[row][column] = cells.Wall()
            for row in range(y + 1,  y + height):
                for column in range(x + 1, x + width):
                    self.tiles[row][column] = cells.Floor()
            return room
        return None

    def gen_corridor_horizontal(self, y, x1, x2):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[y][x] = cells.Floor()

    def gen_corridor_vertical(self, x, y1, y2):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[y][x] = cells.Floor()

    def gen_monsters(self):
        entity_list = []
        for room in self.rooms:
            max_num_monsters = room.get_area() // 15
            num_monsters = libtcod.random_get_int(0, 0, max_num_monsters)
            for i in range(num_monsters):
                x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
                y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)
                if get_blocking_entity(entity_list, x, y) is None and self.tiles[y][x].is_blocked is False:
                    monster = Goblin(x, y)
                    entity_list.append(monster)
        return entity_list

    def gen_dungeon(self):
        self.initialize_dungeon()
        self.rooms = []
        max_num_rooms = self.width * self.height // 50
        num_rooms = 0
        for i in range(max_num_rooms):
            room = self.gen_room()
            if room != None:
                self.rooms.append(room)
                num_rooms += 1
                if num_rooms > 1:
                    x1, y1 = prev_room.get_center()
                    x2, y2 = room.get_center()
                    if libtcod.random_get_int(0, 0, 1) == 1:
                        self.gen_corridor_horizontal(y1, x1, x2)
                        self.gen_corridor_vertical(x2, y1, y2)
                    else:
                        self.gen_corridor_vertical(x1, y1, y2)
                        self.gen_corridor_horizontal(y2, x1, x2)
                prev_room = room
        x, y = self.rooms[0].get_center()
        player = Player(x, y)

        # TODO: remove x and y offset hardcoding
        player.x_offset = int((2 * 17 + 46) / 2 - player.x)
        player.y_offset = int((2* 1 + 46) / 2 - player.y)
        entity_list = self.gen_monsters()
        entity_list.insert(0, player)
        return player, entity_list
