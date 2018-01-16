import libtcodpy as libtcod
import cells, random
from rect import Rect
from map_generation.dungeon_base import Dungeon

class Dungeon_BSP(Dungeon):
    def __init__(self, width, height, depth = 5, min_leaf_size = 10, min_room_size = 5, max_room_area = 36, full_rooms = False):
        super().__init__(width, height)
        self.depth = depth
        self.min_leaf_size = min_leaf_size
        self.min_room_size = min_room_size
        self.max_room_area = max_room_area
        self.full_rooms = full_rooms

    def v_line(self, x, y1, y2):
        if y1 > y2:
            y1, y2 = y2, y1

        for y in range(y1, y2 + 1):
            self.tiles[y][x] = cells.Floor()

    def v_line_up(self, x, y):
        while y >= 0 and self.tiles[y][x].is_blocked == True:
            self.tiles[y][x] = cells.Floor()
            y -= 1

    def v_line_down(self, x, y):
        while y < self.height and self.tiles[y][x].is_blocked == True:
            self.tiles[y][x] = cells.Floor()
            y += 1

    def h_line(self, x1, y, x2):
        if x1 > x2:
            x1, x2 = x2, x1

        for x in range(x1, x2 + 1):
            self.tiles[y][x] = cells.Floor()

    def h_line_left(self, x, y):
        while x >= 0 and self.tiles[y][x].is_blocked == True:
            self.tiles[y][x] = cells.Floor()
            x -= 1
    def h_line_right(self, x, y):
        while x < self.width and self.tiles[y][x].is_blocked == True:
            self.tiles[y][x] = cells.Floor()
            x += 1

    def traverse_node(self, node, dat):
        # Create room
        if libtcod.bsp_is_leaf(node):
            min_x = node.x + 1
            max_x = node.x + node.w - 1
            min_y = node.y + 1
            max_y = node.y + node.h - 1

            if max_x == self.width - 1:
                max_x -= 1
            if max_y == self.height - 1:
                max_y -= 1

            if self.full_rooms == False:
                while True:
                    min_x = libtcod.random_get_int(None, min_x, max_x - self.min_room_size + 1)
                    min_y = libtcod.random_get_int(None, min_y, max_y - self.min_room_size + 1)
                    max_x = libtcod.random_get_int(None, min_x + self.min_room_size - 2, max_x)
                    max_y = libtcod.random_get_int(None, min_y + self.min_room_size - 2, max_y)

                    if (max_x - min_x + 1) * (max_y - min_y + 1) <= self.max_room_area:
                        break

            node.x = min_x
            node.y = min_y
            node.w = max_x - min_x + 1
            node.h = max_y - min_y + 1

            self.dig_room((min_x, max_x), (min_y, max_y))
            self.rooms.append(Rect(node.x, node.y, node.w, node.h))

        # Create corridors
        else:
            left = libtcod.bsp_left(node)
            right = libtcod.bsp_right(node)
            node.x = min(left.x, right.x)
            node.y = min(left.y, right.y)
            node.w = max(left.x + left.w, right.x + right.w) - node.x
            node.h = max(left.y + left.h, right.y + right.h) - node.y

            x1 = int((2 * left.x + left.w) / 2)
            y1 = int((2 * left.y + left.h) / 2)

            x2 = int((2 * right.x + right.w) / 2)
            y2 = int((2 * right.y + right.h) / 2)

            if node.horizontal:
                if left.x + left.w - 1 < right.x or right.x + right.w - 1 < left.x:
                    x1 = libtcod.random_get_int(None, left.x, left.x + left.w - 1)
                    x2 = libtcod.random_get_int(None, right.x, right.x + right.w - 1)
                    y = libtcod.random_get_int(None, left.y + left.h, right.y)
                    self.v_line_up(x1, y - 1)
                    self.h_line(x1, y, x2)
                    self.v_line_down(x2, y + 1)
                else:
                    min_x = max(left.x, right.x)
                    max_x = min(left.x + left.w - 1, right.x + right.w - 1)
                    x = libtcod.random_get_int(None, min_x, max_x)
                    self.v_line_down(x, right.y)
                    self.v_line_up(x, right.y - 1)
            else:
                if left.y + left.h - 1 < right.y or right.y + right.h - 1 < left.y:
                    y1 = libtcod.random_get_int(None, left.y, left.y + left.h - 1)
                    y2 = libtcod.random_get_int(None, right.y, right.y + right.h - 1)
                    x = libtcod.random_get_int(None, left.x + left.w, right.x)
                    self.h_line_left(x - 1, y1)
                    self.v_line(x, y1, y2)
                    self.h_line_right(x + 1, y2)
                else:
                    min_y = max(left.y, right.y)
                    max_y = min(left.y + left.h - 1, right.y + right.h - 1)
                    y = libtcod.random_get_int(None, min_y, max_y)
                    self.h_line_left(right.x - 1, y)
                    self.h_line_right(right.x, y)
        return True

    def gen_dungeon(self, player):
        self.initialize_dungeon()
        self.rooms = []

        # Root node
        bsp = libtcod.bsp_new_with_size(0, 0, self.width, self.height)

        # Split into nodes with recursive algorithm (10 is number of rooms?)(6 is min room size + 1?)(1.5 is max ratio v and h of nodes?)
        libtcod.bsp_split_recursive(bsp, 0, self.depth, self.min_leaf_size + 1, self.min_leaf_size + 1, 1.5, 1.5)

        # Traverse nodes and create rooms
        libtcod.bsp_traverse_inverted_level_order(bsp, self.traverse_node)

        self.gen_stairs(only_in_rooms = True)
        self.set_player_coords(player)
        entity_list = [player]
        self.gen_monsters(entity_list, only_in_rooms = True)
        self.gen_items(entity_list, only_in_rooms = True)
        return entity_list

    def gen_empty_dungeon(self):
        self.initialize_dungeon()
        self.rooms = []

        # Root node
        bsp = libtcod.bsp_new_with_size(0, 0, self.width, self.height)

        # Split into nodes with recursive algorithm (10 is number of rooms?)(6 is min room size + 1?)(1.5 is max ratio v and h of nodes?)
        libtcod.bsp_split_recursive(bsp, 0, self.depth, self.min_leaf_size + 1, self.min_leaf_size + 1, 1.5, 1.5)

        # Traverse nodes and create rooms
        libtcod.bsp_traverse_inverted_level_order(bsp, self.traverse_node)
