import libtcodpy as libtcod
import cells, random
from map_generation.spawn_entities import choose_entity_to_spawn
from entities.entity_functions import get_blocking_entity

# Base dungeon class inherited by all other dungeon generators
class Dungeon:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def initialize_dungeon(self, tile = None):
        # Initialise a dungeon arr with specified tile
        if tile != None:
            self.tiles = [[tile for x in range(self.width)] for y in range(self.height)]
        else:
            self.tiles = [[cells.Rock() for x in range(self.width)] for y in range(self.height)]

    # Generates all the monsters for the dungeon floor
    def gen_monsters(self, player, entity_list, floor_index, only_in_rooms = False):
        xp_sum = 0
        min_required_xp = player.components["level"].level_up_xp

        # While loop ensures player gets at least a certain amount of exp
        while xp_sum < min_required_xp*1.2:
            if only_in_rooms:
                # Randomly choose a room to generate in as well as a point in the room
                room = random.choice(self.rooms)
                x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
                y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)
            else:
                # Randomly choose a point in the dungeon
                x = libtcod.random_get_int(0, 0, self.width - 1)
                y = libtcod.random_get_int(0, 0, self.height - 1)

            # If there is no other solid entity at the point chosen and the cell chosen is not solid
            if get_blocking_entity(entity_list, x, y) is None and self.tiles[y][x].is_blocked is False:
                # Spawn entity, add it to entity list and increment the xp_sum variable
                monster = choose_entity_to_spawn("mob", floor_index)(x,y)
                xp_sum += monster.components["level"].avg_xp_drop
                entity_list.append(monster)

    # Generates all the items for the dungeon floor
    def gen_items(self, entity_list, floor_index, only_in_rooms = False):
        if only_in_rooms:
            # Attempt to gen items in each room
            for room in self.rooms:
                # Choose a random amount of items to attempt spawning, proportional to the size of the room
                max_num_items = room.get_area() // 15
                num_items = libtcod.random_get_int(0, 0, max_num_items)
                # For each item spawn attempt
                for i in range(num_items):
                    # Choose a random point in the room
                    x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
                    y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)
                    # If there are no solid entities at the point and the cell is not solid
                    if get_blocking_entity(entity_list, x, y) is None and self.tiles[y][x].is_blocked is False:
                        # Spawn item and add it to entity list
                        item = choose_entity_to_spawn("item", floor_index)(x,y)
                        entity_list.append(item)
        else:
            # Calculate item spawn attempts proportional to the size of the dungeon
            max_num_items = int((self.height * self.width) * 0.005)
            # For each item spawn attempt
            for i in range(max_num_items):
                # Choose a random point on the dungeon floor
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                # If there are no solid entities at the point and the cell is not solid
                if get_blocking_entity(entity_list, x, y) is None and self.tiles[y][x].is_blocked is False:
                        # Spawn the item and add it to the entity list
                        item = choose_entity_to_spawn("item", floor_index)(x,y)
                        entity_list.append(item)

    # Generate the up and down stairs
    def gen_stairs(self, only_in_rooms = False):
        if only_in_rooms:
            # Calculate points for the stairs
            x1, y1 = self.rooms[0].get_center() # Up stairs in center of the first room
            while True:
                # Choose a random room until the room is not the first room
                x2, y2 = random.choice(self.rooms).get_center()
                if x2 != x1 and y2 != y1:
                    break
            # Set cells to appropriate stair cell and set entrance and exit points of the floor
            self.tiles[y1][x1] = cells.Stair_Up()
            self.tiles[y2][x2] = cells.Stair_Down()
            self.entrance = (x1, y1)
            self.exit = (x2, y2)
        else:
            while True:
                # Pick a random point until the point is not blocked
                x1 = random.randint(0, self.width - 1)
                y1 = random.randint(0, self.height - 1)
                if not self.tiles[y1][x1].is_blocked:
                    while True:
                        # Pick a random point until the point is not blocked and it's not the same point as the first one
                        x2 = random.randint(0, self.width - 1)
                        y2 = random.randint(0, self.height - 1)
                        if x2 != x1 and y2 != y1 and not self.tiles[y2][x2].is_blocked:
                            break
                    break
            # Set cells to appropriate stair cell and set entrance and exit points of the floor
            self.tiles[y1][x1] = cells.Stair_Up()
            self.tiles[y2][x2] = cells.Stair_Down()
            self.entrance = (x1, y1)
            self.exit = (x2, y2)

    # Sets the players offset for the camera
    def set_player_offset(self, player):
        player.x_offset = int((2 * 17 + 46) / 2 - player.x)
        player.y_offset = int((2* 1 + 46) / 2 - player.y)

    def set_player_coords(self, player, rooms = True):
        # Sets the players coordinates in the dungeon
        if rooms:
            player.x, player.y = self.rooms[0].get_center()
            self.set_player_offset(player)
        else:
            player.x, player.y = self.entrance
            self.set_player_offset(player)

    # Digs out a rectangle room in specified x and y ranges
    def dig_room(self, x_range, y_range):
        min_x, max_x = x_range
        min_y, max_y = y_range
        # Place room wall cells
        for y in range(min_y - 1, max_y + 2):
            for x in range(min_x - 1, max_x + 2):
                self.tiles[y][x] = cells.Wall()
        # Place room floor cells
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                self.tiles[y][x] = cells.Floor()
