import libtcodpy as libtcod
from bearlibterminal import terminal
from level import *
from render.render_functions import *
from fov_functions import *
from input_functions import *
from ui import *
from game_states import *
from death_functions import *

# Initialize bearlibterminal terminal
terminal.open()
terminal.set("window: title = 'NEA Project', size = 96x64; font: 'font_12x12.png', size=12x12, codepage=437")
terminal.refresh()

# Set inital game state
game_state = Game_States.PLAYER_TURN

# Initialize UI elements
ui_elements = initialize_ui_elements()

# Initialize dungeon
dungeon = Dungeon(96, 64)
entities, player = dungeon.gen_dungeon_tunneling()

# Initialize FOV
fov_map, fov_recompute = initialize_fov(dungeon)

# Main Loop
while True:
    # Render UI and dungeon
    render(dungeon, player, entities, fov_map, fov_recompute, ui_elements)

    # Get player action as a dict
    player_action = handle_inputs()
    move = player_action.get("move")
    rest = player_action.get("rest")
    quit = player_action.get("quit")

    # If player action is to quit then break the main loop
    if quit:
        break

    # If it is the players turn
    if game_state == Game_States.PLAYER_TURN:
        player_turn_results = []

        # If the player wants to move
        if move:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy
            # If the destination tile is walkable
            if dungeon.tiles[destination_y][destination_x].is_blocked == False:
                # Check if there are any blocking entities at destination
                target = get_blocking_entity(entities, destination_x, destination_y)

                # If there is a blocking entity at destination attack it
                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                # Otherwise move to destination
                else:
                    player.move(dx, dy)
                    fov_recompute = True
                # Player turn is over so set game_state to ENEMY_TURN
                game_state = Game_States.ENEMY_TURN

        # If player has chosen to do nothing
        if rest:
            # Player turn is over so set game_state to ENEMY_TURN
            game_state = Game_States.ENEMY_TURN

        for player_turn_result in player_turn_results:
            message = player_turn_result.get("message")
            dead_entity = player_turn_result.get("dead")

            # If the players turn has generated a message add them to the messages list
            if message:
                ui_elements["messages"].messages.append(message)
            # If the players turn has resulted in an entity dying
            if dead_entity:
                # If the player has died generate an appropriate message and change game_state
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                # Otherwise generate an appropriate message for the entities death
                else:
                    message = kill_monster(dead_entity)
                ui_elements["messages"].messages.append(message)

    # If it is not the players turn
    if game_state == Game_States.ENEMY_TURN:
        # For each entity that has an AI and is not the player
        for entity in entities:
            if entity.ai and entity != player:
                # Simulate entity turn and get results
                enemy_turn_results = entity.ai.take_turn(player, fov_map, dungeon, entities)

                for enemy_turn_result in enemy_turn_results:
                    message = enemy_turn_result.get("message")
                    dead_entity = enemy_turn_result.get("dead")

                    # If entity turn has generated a message add it to the messages list
                    if message:
                        ui_elements["messages"].messages.append(message)
                    # If the entities turn has resulted in an entity dying
                    if dead_entity:
                        # If the player has died generate an appropriate message and change game_state
                        if dead_entity == player:
                            message, game_state = kill_player(dead_entity)
                        # Otherwise generate an appropriate message for the entities death
                        else:
                            message = kill_monster(dead_entity)
                        ui_elements["messages"].messages.append(message)
                # If the player has died during the entities turn break the for loop and stop simulating entity turns
                if game_state == Game_States.PLAYER_DEAD:
                    break
        # If the player does not die as a result of an entities turn set game_state to PLAYER_TURN
        else:
            game_state = Game_States.PLAYER_TURN

terminal.close()
