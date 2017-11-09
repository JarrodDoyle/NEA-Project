from enum import Enum
from bearlibterminal import terminal
from initialize import initialize_move_keybinds

class Move_Keybinds:
    KEY_DICT = initialize_move_keybinds()
    MOVE_N = KEY_DICT.get("MOVE_N")
    MOVE_NE = KEY_DICT.get("MOVE_NE")
    MOVE_E = KEY_DICT.get("MOVE_E")
    MOVE_SE = KEY_DICT.get("MOVE_SE")
    MOVE_S = KEY_DICT.get("MOVE_S")
    MOVE_SW = KEY_DICT.get("MOVE_SW")
    MOVE_W = KEY_DICT.get("MOVE_W")
    MOVE_NW = KEY_DICT.get("MOVE_NW")
    REST = KEY_DICT.get("REST")

class Command_Keybinds:
    PICK_UP = terminal.TK_G
    OPEN_INVENTORY = terminal.TK_I
    TOGGLE_FOG = terminal.TK_P


