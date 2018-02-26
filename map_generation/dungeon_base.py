import libtcodpy as libtcod
import cells, random
from map_generation.spawn_entities import choose_entity_to_spawn
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

    def gen_monsters(self, player, entity_list, floor_index, only_in_rooms = False):
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
                monster = choose_entity_to_spawn("mob", floor_index)(x,y)
                xp_sum += monster.components["level"].avg_xp_drop
                entity_list.append(monster)

    def gen_items(self, entity_list, floor_index, only_in_rooms = False):
        if only_in_rooms:
            for room in self.rooms:
                max_num_items = room.get_area() // 15
                num_items = libtcod.random_get_int(0, 0, max_num_items)
                for i in range(num_items):
                    x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
                    y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)
                    if get_blocking_entity(entity_list, x, y) is None and self.tiles[y][x].is_blocked is False:
                        item = choose_entity_to_spawn("item", floor_index)(x,y)
                        entity_list.append(item)
        else:
            max_num_items = int((self.height * self.width) * 0.015)
            for i in range(max_num_items):
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                if get_blocking_entity(entity_list, x, y) is None and self.tiles[y][x].is_blocked is False:
                        item = choose_entity_to_spawn("item", floor_index)(x,y)
                        entity_list.append(item)

    def gen_stairs(self, only_in_rooms = False):
        if only_in_rooms:
            x1, y1 = self.rooms[0].get_center()
            while True:
                x2, y2 = random.choice(self.rooms).get_center()
                if x2 != x1 and y2 != y1:
                    break
            self.tiles[y1][x1] = cells.Stair_Up()
            self.tiles[y2][x2] = cells.Stair_Down()
            self.entrance = (x1, y1)
            self.exit = (x2, y2)
        else:
            while True:
                x1 = random.randint(0, self.width - 1)
                y1 = random.randint(0, self.height - 1)
                if not self.tiles[y1][x1].is_blocked:
                    while True:
                        x2 = random.randint(0, self.width - 1)
                        y2 = random.randint(0, self.height - 1)
                        if x2 != x1 and y2 != y1 and not self.tiles[y2][x2].is_blocked:
                            break
                    break
            self.tiles[y1][x1] = cells.Stair_Up()
            self.tiles[y2][x2] = cells.Stair_Down()
            self.entrance = (x1, y1)
            self.exit = (x2, y2)

    def set_player_offset(self, player):
        player.x_offset = int((2 * 17 + 46) / 2 - player.x)
        player.y_offset = int((2* 1 + 46) / 2 - player.y)

    def set_player_coords(self, player, rooms = True):
        if rooms:
            player.x, player.y = self.rooms[0].get_center()
            self.set_player_offset(player)
        else:
            player.x, player.y = self.entrance
            self.set_player_offset(player)

    def dig_room(self, x_range, y_range):
        min_x, max_x = x_range
        min_y, max_y = y_range

        for y in range(min_y - 1, max_y + 2):
            for x in range(min_x - 1, max_x + 2):
                self.tiles[y][x] = cells.Wall()
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                self.tiles[y][x] = cells.Floor()
