import random
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

class Game:
    def __init__(self):
        # Set inital game state
        self.game_state = Game_States.PLAYER_TURN
        self.previous_game_state = self.game_state

        # Initialize UI elements and player
        self.ui_elements = initialize_ui_elements()
        self.player = Player(0,0)

        # Initialize dungeon
        if random.randint(0, 1):
            self.dungeon = Dungeon_BSP(width = 96, height = 64, depth = 10, min_leaf_size = 7, min_room_size = 5, max_room_area = 36, full_rooms = False)
        else:
            self.dungeon = Dungeon_Cellular_Automata(width = 96, height = 64, birth_limit = 4, death_limit = 3, chance_to_be_alive = 40, num_steps = 4)
        self.entities = self.dungeon.gen_dungeon(self.player)

        # Initialize FOV
        self.fov_map, self.fov_recompute = initialize_fov(self.dungeon)
        self.fog_of_war = True

    def play(self):
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
            return False

        # If it is the players turn
        if self.game_state == Game_States.PLAYER_TURN:
            player_turn_results = []

            # Toggle fog of war
            if player_action.get("toggle_fog"):
                self.fog_of_war = not self.fog_of_war

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
            if player_action.get("stair_down"):
                if self.dungeon.tiles[self.player.y][self.player.x].cell_name == "stair_down":
                    message = "go to next floor buddy"
                    self.ui_elements["messages"].messages.append(message)
                    if random.randint(0, 1):
                        self.dungeon = Dungeon_BSP(width = 96, height = 64, depth = 10, min_leaf_size = 7, min_room_size = 5, max_room_area = 36, full_rooms = False)
                    else:
                        self.dungeon = Dungeon_Cellular_Automata(width = 96, height = 64, birth_limit = 4, death_limit = 3, chance_to_be_alive = 40, num_steps = 4)
                    self.entities = dungeon.gen_dungeon(self.player)
                    self.fov_map, self.fov_recompute = initialize_fov(self.dungeon)
                else:
                    message = "There are no stairs here."
                    self.ui_elements["messages"].messages.append(message)

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
                        messages.append(player.components["level"].gain_xp(xp))
                    for message in messages:
                        self.ui_elements["messages"].messages.append(message)

                # If the player picked up an item
                if item_added:
                    # Remove item from entities list and therefore the dungeon map. Change game state to enemy turn
                    self.entities.remove(item_added)
                    self.game_state = Game_States.ENEMY_TURN

        # If player looking at an item in inventory
        if self.game_state == Game_States.USING_ITEM:
            description = "{}\n Us(e)\n (d)rop\n E(x)amine".format(item.name)
            self.ui_elements["description"].text = description

            use = player_action.get("use")
            drop = player_action.get("drop")
            examine = player_action.get("examine")

            if use:
                message = item.components["item"].use(self.player, self.player.components["inventory"])
                self.ui_elements["messages"].messages.append(message)
                self.game_state = Game_States.PLAYER_TURN
            if drop:
                self.player.components["inventory"].items.remove(item)
                item.x = self.player.x
                item.y = self.player.y
                self.entities.append(item)
                message = "You drop the {} on the ground.".format(item.name)
                self.ui_elements["messages"].messages.append(message)
                self.game_state = Game_States.PLAYER_TURN
            if examine:
                self.ui_elements["description"].text = item.description
                message = "You decide to look more closely at the {}.".format(item.name)
                self.ui_elements["messages"].messages.append(message)

            if cancel:
                self.game_state = Game_States.INVENTORY_ACTIVE

        # If player is using the inventory
        if self.game_state == Game_States.INVENTORY_ACTIVE:
            if inventory_index is not None:
                if inventory_index < len(self.player.components["inventory"].items):
                    item = self.player.components["inventory"].items[inventory_index]
                    message = "You look at the {}.".format(item.name)
                    description = "{}\n Us(e)\n (d)rop\n E(x)amine".format(item.name)
                    self.ui_elements["description"].text = description
                    self.game_state = Game_States.USING_ITEM
                else:
                    message = "No valid item at index {}".format(inventory_index)
                self.ui_elements["messages"].messages.append(message)
            elif cancel:
                self.game_state = previous_game_state

        # If it is not the players turn
        if self.game_state == Game_States.ENEMY_TURN:
            # For each entity that has an AI and is not the player
            for entity in self.entities:
                if entity != self.player and entity.x == self.player.x and entity.y == self.player.y:
                    ui_elements["description"].text = entity.description
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

        if self.game_state == Game_States.PLAYER_DEAD:
            if player_action.get("quit"):
                return False
        return True
