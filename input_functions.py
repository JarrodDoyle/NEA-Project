from bearlibterminal import terminal

def handle_inputs():
    key = terminal.read()
    if key == terminal.TK_CLOSE:
        return {"quit": True}

    elif key == terminal.TK_KP_8:
        return {"move": (0, -1)}
        #player.move_or_attack(dungeon, 0, -1)
    elif key == terminal.TK_KP_4:
        return {"move": (-1, 0)}
        #player.move_or_attack(dungeon, -1, 0)
    elif key == terminal.TK_KP_6:
        return {"move": (1, 0)}
        #player.move_or_attack(dungeon, 1, 0)
    elif key == terminal.TK_KP_2:
        return {"move": (0, 1)}
        #player.move_or_attack(dungeon, 0, 1)
    elif key == terminal.TK_KP_7:
        return {"move": (-1, -1)}
        #player.move_or_attack(dungeon, -1, -1)
    elif key == terminal.TK_KP_9:
        return {"move": (1, -1)}
        #player.move_or_attack(dungeon, 1, -1)
    elif key == terminal.TK_KP_1:
        return {"move": (-1, 1)}
        #player.move_or_attack(dungeon, -1, 1)
    elif key == terminal.TK_KP_3:
        return {"move": (1, 1)}
        #player.move_or_attack(dungeon, 1, 1)
    elif key == terminal.TK_KP_5:
        return {"rest": True}

    else:
        return {}
