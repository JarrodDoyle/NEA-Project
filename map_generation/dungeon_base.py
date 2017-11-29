import libtcodpy as libtcod
import cells
from entities.items import Health_Pot
from entities.mobs import Goblin
from entities.entity_functions import get_blocking_entity

class Dungeon:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def initialize_dungeon(self):
        self.tiles = [[cells.Rock() for x in range(self.width)] for y in range(self.height)]

    def gen_monsters(self, entity_list):
        for room in self.rooms:
            max_num_monsters = room.get_area() // 15
            num_monsters = libtcod.random_get_int(None, 0, max_num_monsters)
            for i in range(num_monsters):
                x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
                y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)
                if get_blocking_entity(entity_list, x, y) is None and self.tiles[y][x].is_blocked is False:
                    monster = Goblin(x, y)
                    entity_list.append(monster)

    def gen_items(self, entity_list):
        for room in self.rooms:
            max_num_items = room.get_area() // 15
            num_items = libtcod.random_get_int(0, 0, max_num_items)
            for i in range(num_items):
                x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
                y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)
                if get_blocking_entity(entity_list, x, y) is None and self.tiles[y][x].is_blocked is False:
                    item = Health_Pot(x, y)
                    entity_list.append(item)

    def dig_room(self, x_range, y_range):
        min_x, max_x = x_range
        min_y, max_y = y_range

        for y in range(min_y - 1, max_y + 2):
            for x in range(min_x - 1, max_x + 2):
                self.tiles[y][x] = cells.Wall()
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                self.tiles[y][x] = cells.Floor()
