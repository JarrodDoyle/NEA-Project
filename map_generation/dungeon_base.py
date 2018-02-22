import libtcodpy as libtcod
import cells, random
from map_generation.spawn_entities import choose_item_to_spawn, choose_mob_to_spawn
from entities.entity_functions import get_blocking_entity

class Dungeon:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def initialize_dungeon(self, tile = None):
        if tile != None:
            self.tiles = [[tile for x in range(self.width)] for y in range(self.height)]
        else:
            self.tiles = [[cells.Rock() for x in range(self.width)] for y in range(self.height)]

    def gen_monsters(self, player, entity_list, only_in_rooms = False):
        xp_sum = 0
        min_required_xp = player.components["level"].level_up_xp
        
        while xp_sum < min_required_xp*1.2:
            if only_in_rooms:
                room = random.choice(self.rooms)
                x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
                y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)
            else:
                x = libtcod.random_get_int(0, 0, self.width - 1)
                y = libtcod.random_get_int(0, 0, self.height - 1)

            if get_blocking_entity(entity_list, x, y) is None and self.tiles[y][x].is_blocked is False:
                monster = choose_mob_to_spawn()(x,y)
                xp_sum += monster.components["level"].avg_xp_drop
                entity_list.append(monster)

    def gen_items(self, entity_list, only_in_rooms = False):
        if only_in_rooms:
            for room in self.rooms:
                max_num_items = room.get_area() // 15
                num_items = libtcod.random_get_int(0, 0, max_num_items)
                for i in range(num_items):
                    x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
                    y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)
                    if get_blocking_entity(entity_list, x, y) is None and self.tiles[y][x].is_blocked is False:
                        item = choose_item_to_spawn()(x,y)
                        entity_list.append(item)
        else:
            max_num_items = int((self.height * self.width) * 0.015)
            for i in range(max_num_items):
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                if get_blocking_entity(entity_list, x, y) is None and self.tiles[y][x].is_blocked is False:
                        item = choose_item_to_spawn()(x,y)
                        entity_list.append(item)

    def gen_stairs(self, only_in_rooms = False):
        if only_in_rooms:
            x, y = random.choice(self.rooms).get_center()
            self.tiles[y][x] = cells.Stair_Down()
        else:
            while True:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                if not self.tiles[y][x].is_blocked:
                    break
            self.tiles[y][x] = cells.Stair_Down()

    def set_player_coords(self, player, rooms = True):
        if rooms:
            player.x, player.y = random.choice(self.rooms).get_center()
            player.x_offset = int((2 * 17 + 46) / 2 - player.x)
            player.y_offset = int((2* 1 + 46) / 2 - player.y)
        else:
            while True:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                if not self.tiles[y][x].is_blocked:
                    player.x = x
                    player.y = y
                    player.x_offset = int((2 * 17 + 46) / 2 - player.x + 1)
                    player.y_offset = int((2* 1 + 46) / 2 - player.y + 1)
                    break

    def dig_room(self, x_range, y_range):
        min_x, max_x = x_range
        min_y, max_y = y_range

        for y in range(min_y - 1, max_y + 2):
            for x in range(min_x - 1, max_x + 2):
                self.tiles[y][x] = cells.Wall()
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                self.tiles[y][x] = cells.Floor()
