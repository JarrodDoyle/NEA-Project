from bearlibterminal import terminal
import configparser

def load_terminal_settings():
    settings = open("config/terminal_settings.cfg", "r")
    return "; ".join([i.strip() for i in settings.readlines()])

def initialize_terminal():
    terminal.open()
    terminal.set(load_terminal_settings())
    terminal.refresh()

def initialize_dungeon():
    return Dungeon_BSP(width = 96, height = 64, depth = 10, min_leaf_size = 7, min_room_size = 5, max_room_area = 36, full_rooms = False)

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
