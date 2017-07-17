import libtcodpy as libtcod
import cells, entities
from rect import *

def gen_blank(width, height):
    level = [[cells.Rock() for x in range(width)] for y in range(height)]
    return level

def gen_room(level):
    width = libtcod.random_get_int(None, 4, 8)
    height = libtcod.random_get_int(None, 4, 8)
    x = libtcod.random_get_int(None, 0, len(level[0]) - 1 - width)
    y = libtcod.random_get_int(None, 0, len(level) - 1 - height)

    valid_room = True
    for row in range(y, y + height + 1):
        for column in range(x, x + width + 1):
            if level[row][column].cell_name != "rock":
                valid_room = False

    if valid_room:
        room = Rect(x, y, width, height)
        for row in range(y, y + height + 1):
            for column in  range(x, x + width + 1):
                level[row][column] = cells.Wall()
        for row in range(y + 1,  y + height):
            for column in range(x + 1, x + width):
                level[row][column] = cells.Floor()
        return room
    return None

def gen_rooms(dungeon):
    max_num_rooms = len(dungeon) * len(dungeon[0]) // 50
    num_rooms = 0
    rooms = []
    for i in range(max_num_rooms):
        room = gen_room(dungeon)
        if room != None:
            rooms.append(room)
            num_rooms += 1
            if num_rooms > 1:
                x1, y1 = prev_room.get_center()
                x2, y2 = room.get_center()
                if libtcod.random_get_int(0, 0, 1) == 1:
                    gen_corridor_horizontal(dungeon, y1, x1, x2)
                    gen_corridor_vertical(dungeon, x2, y1, y2)
                else:
                    gen_corridor_vertical(dungeon, x1, y1, y2)
                    gen_corridor_horizontal(dungeon, y2, x1, x2)
            prev_room = room
    return rooms

def gen_corridor_horizontal(dungeon, y, x1, x2):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        dungeon[y][x] = cells.Floor()

def gen_corridor_vertical(dungeon, x, y1, y2):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        dungeon[y][x] = cells.Floor()

def gen_monsters(dungeon, rooms):
    entity_list = []
    for room in rooms:
        max_num_monsters = room.get_area() // 15
        num_monsters = libtcod.random_get_int(0, 0, max_num_monsters)
        for i in range(num_monsters):
            x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
            y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)
            if dungeon[y][x].entity is None and dungeon[y][x].is_blocked is False:
                goblin = entities.Goblin(x, y)
                dungeon[y][x].add_entity(goblin)
                entity_list.append(goblin)
    return entity_list

def gen_dungeon(width, height):
    dungeon = gen_blank(width, height)
    rooms = gen_rooms(dungeon)
    x, y = rooms[0].get_center()
    player = entities.Player(x, y)
    #player.x_offset = width // 2 - player.x
    #player.y_offset = height // 2 - player.y

    # TODO: remove x and y offset hardcoding
    player.x_offset = int((2 * 17 + 46) / 2 - player.x)
    player.y_offset = int((2* 1 + 46) / 2 - player.y)
    dungeon[y][x].add_entity(player)
    entity_list = gen_monsters(dungeon, rooms)
    entity_list.insert(0, player)
    return dungeon, entity_list, player
