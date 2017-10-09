from bearlibterminal import terminal

def load_settings():
    settings = open("config/settings.cfg", "r")
    return "; ".join([i.strip() for i in settings.readlines()])

def initialize_terminal():
    terminal.open()
    terminal.set(load_settings())
    terminal.refresh()

def initialize_dungeon():
    return Dungeon_BSP(width = 96, height = 64, depth = 10, min_leaf_size = 7, min_room_size = 5, max_room_area = 36, full_rooms = False)
