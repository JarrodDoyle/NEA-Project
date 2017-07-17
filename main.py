import libtcodpy as libtcod
from bearlibterminal import terminal
from level import *
from render_functions import *
from fov_functions import *
from input_functions import *

# Initialisation
terminal.open()
terminal.set("window: title = 'NEA Project', size = 96x64; font: 'font_12x12.png', size=12x12, codepage=437")
terminal.refresh()

dungeon, entities, player = gen_dungeon(96, 64)
fov_map, fov_recompute = initialize_fov(dungeon)

while True:
    render(dungeon, player, entities, fov_map, fov_recompute)

    player_action = handle_inputs()
    if player_action.get("quit") == True:
        break

    if player_action.get("move"):
        direction = player_action.get("move")
        player.move_or_attack(dungeon, direction[0], direction[1])
        fov_recompute = True
        dead_entities = []
        for entity in entities:
            if entity.fighter and entity.fighter.hp <= 0:
                dungeon[entity.y][entity.x].remove_entity()
                player.messages.append("You killed the {}.".format(entity.name))
                dead_entities.append(entity)
        for entity in dead_entities:
            entities.remove(entity)
terminal.close()
