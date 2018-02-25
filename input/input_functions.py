from bearlibterminal import terminal
from game_states import Game_States
from input.keybindings import *

def handle_player_turn_inputs():
    key = terminal.read()
    if key == terminal.TK_CLOSE:
        return {"quit": True}
    elif key == terminal.TK_ESCAPE:
        return {"cancel": True}

    elif key == Move_Keybinds.MOVE_N:
        return {"move": (0, -1)}
    elif key == Move_Keybinds.MOVE_W:
        return {"move": (-1, 0)}
    elif key == Move_Keybinds.MOVE_E:
        return {"move": (1, 0)}
    elif key == Move_Keybinds.MOVE_S:
        return {"move": (0, 1)}
    elif key == Move_Keybinds.MOVE_NW:
        return {"move": (-1, -1)}
    elif key == Move_Keybinds.MOVE_NE:
        return {"move": (1, -1)}
    elif key == Move_Keybinds.MOVE_SW:
        return {"move": (-1, 1)}
    elif key == Move_Keybinds.MOVE_SE:
        return {"move": (1, 1)}
    elif key == Move_Keybinds.REST:
        return {"rest": True}

    elif key == Command_Keybinds.PICK_UP:
        return {"pickup": True}
    elif key == Command_Keybinds.OPEN_INVENTORY:
        return {"inventory_active": True}
    elif key == Command_Keybinds.TOGGLE_FOG:
        return {"toggle_fog": True}
    elif key == Command_Keybinds.TARGET:
        return {"target": True}
    if terminal.state(terminal.TK_SHIFT):
        key += terminal.TK_SHIFT
        if key == Command_Keybinds.STAIR_DOWN or key == Command_Keybinds.STAIR_UP:
            return {"stair_used": True}

    return {}

def handle_player_dead_inputs():
    key = terminal.read()
    if key == terminal.TK_CLOSE:
        return {"quit": True}
    elif key == terminal.TK_ESCAPE:
        return {"cancel": True}
    return {}

def handle_inventory_inputs():
    key = terminal.read()
    if key == terminal.TK_ESCAPE:
        return {"cancel": True}
    if key == terminal.TK_CLOSE:
        return {"quit": True}

    index = key - 4
    if index >= 0:
        return {"inventory_index": index}

def handle_inputs(game_state):
    if game_state == Game_States.PLAYER_TURN:
        return handle_player_turn_inputs()
    elif game_state == Game_States.PLAYER_DEAD:
        return handle_player_dead_inputs()
    elif game_state == Game_States.INVENTORY_ACTIVE:
        return handle_inventory_inputs()
    elif game_state == Game_States.USING_ITEM:
        return item_inputs()

    return {}

def item_inputs():
    key = terminal.read()
    if key == terminal.TK_E:
        return {"use": True}
    elif key == terminal.TK_D:
        return {"drop": True}
    elif key == terminal.TK_X:
        return {"examine": True}

    if key == terminal.TK_CLOSE:
        return {"quit": True}
    elif key == terminal.TK_ESCAPE:
        return {"cancel": True}
    return {}
