from bearlibterminal import terminal
import random
from map_generation.bsp_map import Dungeon_BSP
from map_generation.cellular_automata import Dungeon_Cellular_Automata
from map_generation.mazes_and_rooms import Dungeon_Mazes_And_Rooms
from map_generation.rogue import Dungeon_Rogue
from create_character import Character_Creation
from entities.mobs import Player

def load_terminal_settings():
    settings = open("config/terminal_settings.cfg", "r")
    return "; ".join([i.strip() for i in settings.readlines()])

def initialize_terminal():
    terminal.open()
    terminal.set(load_terminal_settings())
    terminal.bkcolor("black")
    terminal.color("white")
    terminal.refresh()

def initialize_dungeon(player):
    dungeon_variants = [0,1,2,3]
    variant = random.choice(dungeon_variants)
    if variant == 0:
        dungeon = Dungeon_BSP(width = 96, height = 64, depth = 10, min_leaf_size = 7, min_room_size = 5, max_room_area = 36, full_rooms = False)
        entities = dungeon.gen_dungeon(player)
        return dungeon, entities
    elif variant == 1:
        dungeon = Dungeon_Cellular_Automata(width = 96, height = 64, birth_limit = 4, death_limit = 3, chance_to_be_alive = 40, num_steps = 4)
        entities = dungeon.gen_dungeon(player)
        return dungeon, entities
    elif variant == 2:
        dungeon = Dungeon_Mazes_And_Rooms(width = 95, height = 63)
        entities = dungeon.gen_dungeon(player, attempts = 100)
        return dungeon, entities
    elif variant == 3:
        dungeon = Dungeon_Rogue(width = 96, height = 64, rows = 3, columns = 4)
        entities = dungeon.gen_dungeon(player)
        return dungeon, entities

def initialize_move_keybinds():
    file = open("config/keybindings/move_keys.cfg", "r")
    keybinds = {}
    key_vals = []
    for i in file.readlines():
        equals_index = i.index("=")
        key = i[:equals_index].strip()
        value = int(i[equals_index + 1:].strip())
        keybinds[key] = value
    return keybinds

def initialize_player():
    creator_class = Character_Creation()
    player_name = creator_class.choose_name()
    player_class = creator_class.choose_class()
    return Player(0, 0, player_name, player_class)
