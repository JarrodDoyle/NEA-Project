import random, targetting
from map_generation.bsp_map import Dungeon_BSP
from map_generation.cellular_automata import Dungeon_Cellular_Automata
from fov_functions import *
from render.render_functions import render
from input.input_functions import *
from ui import *
from game_states import Game_States
from entities.mobs import Player
from death_functions import kill_player, kill_monster
from entities.entity_functions import get_blocking_entity
from initialize import initialize_dungeon, initialize_player

class Game:
    def __init__(self):
        # Set inital game state
        self.game_state = Game_States.PLAYER_TURN
        self.previous_game_state = self.game_state

        # Initialize UI elements and dummy player
        self.ui_elements = initialize_ui_elements()
        self.player = initialize_player()

        # Initialize dungeon
        self.dungeon, self.entities = initialize_dungeon(self.player)
        self.floors = [[self.dungeon, self.entities]]
        self.floor_index = 0

        # Initialize FOV
        self.fov_map, self.fov_recompute = initialize_fov(self.dungeon)
        self.fog_of_war = True

        # Initialize final player
        render(player = self.player, entities = self.entities, fov_map = self.fov_map, fov_recompute = self.fov_recompute, ui_elements = self.ui_elements, fog_of_war = self.fog_of_war)

    def play(self):
        result = {}

        # Render UI and dungeon
        render(self.dungeon, self.player, self.entities, self.fov_map, self.fov_recompute, self.ui_elements, self.fog_of_war)

        # Get player action as a dict
        player_action = handle_inputs(self.game_state)
        move = player_action.get("move")
        rest = player_action.get("rest")
        pickup = player_action.get("pickup")
        inventory_active = player_action.get("inventory_active")
        inventory_index = player_action.get("inventory_index")
        cancel = player_action.get("cancel")
        quit = player_action.get("quit")

        # If player action is to quit then break the main loop
        if quit:
            result["quit"] = True

        # If it is the players turn
        if self.game_state == Game_States.PLAYER_TURN:
            if cancel:
                result["cancel"] = True

            player_turn_results = []

            # Toggle fog of war
            if player_action.get("toggle_fog"):
                self.fog_of_war = not self.fog_of_war

            if player_action.get("target"):
                weapon = self.player.components["equipment"].equipment["hands"]
                if weapon is not None:
                    target_range = weapon.components["weapon"].attack_range
                else:
                    target_range = 1

                targetting_result = targetting.choose_target(self.player, self.entities, target_range, entity_type = "fighter")
                if targetting_result.get("target"):
                    target = targetting_result.get("target")
                    player_turn_results.extend(self.player.components["fighter"].attack(target))
                    self.game_state = Game_States.ENEMY_TURN
                elif targetting_result.get("cancel"):
                    pass
                elif targetting_result.get("quit"):
                    result["quit"] = True
                    return result

            # If the player wants to move
            if move:
                dx, dy = move
                destination_x = self.player.x + dx
                destination_y = self.player.y + dy
                # If the destination tile is walkable
                if not self.dungeon.tiles[destination_y][destination_x].is_blocked:
                    # Check if there are any blocking entities at destination
                    target = get_blocking_entity(self.entities, destination_x, destination_y)

                    # If there is a blocking entity at destination attack it
                    if target:
                        attack_results = self.player.components["fighter"].attack(target)
                        player_turn_results.extend(attack_results)
                    # Otherwise move to destination
                    else:
                        self.player.move(dx, dy)
                        self.fov_recompute = True
                    # Player turn is over so set game_state to ENEMY_TURN
                    self.game_state = Game_States.ENEMY_TURN

            # If player has chosen to do nothing
            if rest:
                # Player turn is over so set game_state to ENEMY_TURN
                self.game_state = Game_States.ENEMY_TURN

            # If player tries to pick something up
            if pickup:
                for entity in self.entities:
                    if entity.components.get("item") and entity.x == self.player.x and entity.y == self.player.y:
                        pickup_results = self.player.components["inventory"].add_item(entity)
                        break
                else:
                    pickup_results = [{"message": "[color=yellow]There is nothing here to pick up."}]
                player_turn_results.extend(pickup_results)

            # GO DOWN A FLOOR BOI
            if player_action.get("stair_used"):
                if self.dungeon.tiles[self.player.y][self.player.x].cell_name == "stair_down":
                    self.floor_index += 1
                    if self.floor_index >= len(self.floors):
                        self.dungeon, self.entities = initialize_dungeon(self.player)
                        self.floors.append([self.dungeon, self.entities])
                    else:
                        self.dungeon, self.entities = self.floors[self.floor_index]
                        self.player.x, self.player.y = self.dungeon.exit
                        self.dungeon.set_player_offset(self.player)
                    message = "go to next floor buddy"
                elif self.dungeon.tiles[self.player.y][self.player.x].cell_name == "stair_up":
                    if self.floor_index > 0:
                        self.floor_index -= 1
                        self.dungeon, self.entities = self.floors[self.floor_index]
                        self.player.x, self.player.y = self.dungeon.exit
                        self.dungeon.set_player_offset(self.player)
                        message = "go to previous floor buddy"
                    else:
                        message = "cant go any higher"
                self.ui_elements["messages"].messages.append(message)
                self.fov_map, self.fov_recompute = initialize_fov(self.dungeon)

            # If player accesses inventory
            if inventory_active:
                self.previous_game_state = self.game_state
                self.game_state = Game_States.INVENTORY_ACTIVE
                message = "You open your inventory."
                self.ui_elements["messages"].messages.append(message)

            for player_turn_result in player_turn_results:
                message = player_turn_result.get("message")
                dead_entity = player_turn_result.get("dead")
                item_added = player_turn_result.get("item_added")

                # If the players turn has generated a message add them to the messages list
                if message:
                    self.ui_elements["messages"].messages.append(message)

                # If the players turn has resulted in an entity dying
                if dead_entity:
                    messages = []
                    # If the player has died generate an appropriate message and change game_state
                    if dead_entity == self.player:
                        message, self.game_state = kill_player(dead_entity)
                        messages.append[message]
                    # Otherwise generate an appropriate message for the entities death
                    else:
                        messages.append(kill_monster(dead_entity))
                        xp = dead_entity.components["level"].drop_xp()
                        messages.append(self.player.components["level"].gain_xp(xp))
                    for message in messages:
                        self.ui_elements["messages"].messages.append(message)

                # If the player picked up an item
                if item_added:
                    # Remove item from entities list and therefore the dungeon map. Change game state to enemy turn
                    self.entities.remove(item_added)
                    self.game_state = Game_States.ENEMY_TURN

        # If player is using the inventory
        if self.game_state == Game_States.INVENTORY_ACTIVE:
            if inventory_index is not None:
                if inventory_index < len(self.player.components["inventory"].items):
                    self.item = self.player.components["inventory"].items[inventory_index]
                    message = "You look at the {}.".format(self.item.name)
                    description = "{}\n Us(e)\n (d)rop\n E(x)amine".format(self.item.name)
                    self.ui_elements["description"].text = description
                    self.game_state = Game_States.USING_ITEM
                else:
                    message = "No valid item at index {}".format(inventory_index)
                self.ui_elements["messages"].messages.append(message)
            elif cancel:
                message = "You close your inventory."
                self.ui_elements["messages"].messages.append(message)
                self.game_state = self.previous_game_state

        # If player looking at an item in inventory
        if self.game_state == Game_States.USING_ITEM:
            description = "{}\n Us(e)\n (d)rop\n E(x)amine".format(self.item.name)
            self.ui_elements["description"].text = description

            use = player_action.get("use")
            drop = player_action.get("drop")
            examine = player_action.get("examine")

            if use:
                message = self.item.components["item"].use(self.player, self.player.components["inventory"])
                self.ui_elements["messages"].messages.append(message)
                self.game_state = Game_States.INVENTORY_ACTIVE
            if drop:
                self.item.components["item"].drop(self.entities, self.player, self.player.components["inventory"])
                message = "You drop the {} on the ground.".format(self.item.name)
                self.ui_elements["messages"].messages.append(message)
                self.game_state = Game_States.INVENTORY_ACTIVE
            if examine:
                self.ui_elements["description"].text = self.item.description
                message = "You decide to look more closely at the {}.".format(self.item.name)
                self.ui_elements["messages"].messages.append(message)

            if cancel:
                self.game_state = Game_States.INVENTORY_ACTIVE


        # If it is not the players turn
        if self.game_state == Game_States.ENEMY_TURN:
            # For each entity that has an AI and is not the player
            for entity in self.entities:
                if entity != self.player and entity.x == self.player.x and entity.y == self.player.y:
                    self.ui_elements["description"].text = entity.description
                if entity.components.get("ai") and entity != self.player:
                    # Simulate entity turn and get results
                    enemy_turn_results = entity.components["ai"].take_turn(self.player, self.fov_map, self.dungeon, self.entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get("message")
                        dead_entity = enemy_turn_result.get("dead")

                        # If entity turn has generated a message add it to the messages list
                        if message:
                            self.ui_elements["messages"].messages.append(message)
                        # If the entities turn has resulted in an entity dying
                        if dead_entity:
                            # If the player has died generate an appropriate message and change game_state
                            if dead_entity == self.player:
                                message, self.game_state = kill_player(dead_entity)
                            # Otherwise generate an appropriate message for the entities death
                            else:
                                message = kill_monster(dead_entity)
                            self.ui_elements["messages"].messages.append(message)
                    # If the player has died during the entities turn break the for loop and stop simulating entity turns
                    if self.game_state == Game_States.PLAYER_DEAD:
                        break
            # If the player does not die as a result of an entities turn set game_state to PLAYER_TURN
            else:
                self.game_state = Game_States.PLAYER_TURN

        return result
