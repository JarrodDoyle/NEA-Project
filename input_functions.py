from bearlibterminal import terminal
from game_states import Game_States

def handle_player_turn_inputs():
    key = terminal.read()
    if key == terminal.TK_CLOSE:
        return {"quit": True}

    elif key == terminal.TK_KP_8:
        return {"move": (0, -1)}
    elif key == terminal.TK_KP_4:
        return {"move": (-1, 0)}
    elif key == terminal.TK_KP_6:
        return {"move": (1, 0)}
    elif key == terminal.TK_KP_2:
        return {"move": (0, 1)}
    elif key == terminal.TK_KP_7:
        return {"move": (-1, -1)}
    elif key == terminal.TK_KP_9:
        return {"move": (1, -1)}
    elif key == terminal.TK_KP_1:
        return {"move": (-1, 1)}
    elif key == terminal.TK_KP_3:
        return {"move": (1, 1)}
    elif key == terminal.TK_KP_5:
        return {"rest": True}

    if key == terminal.TK_G:
        return {"pickup": True}
    elif key == terminal.TK_I:
        return {"inventory_active": True}

    else:
        return {}

def handle_player_dead_inputs():
    key = terminal.read()
    if key == terminal.TK_CLOSE:
        return {"quit": True}
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
