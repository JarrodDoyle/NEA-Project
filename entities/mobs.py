from components.fighter import *
from components.ai import *
from components.inventory import *
from render.render_classes import Render_Order
from entities.entity_classes import Entity

class Player(Entity):
    # Initialization of player entity
    def __init__(self, x, y):
        # Inializing the players components
        # hp = 100, strength = 4, defense = 1, accuracy = 4, intelligence = 0
        # hp = 100, strength = 400, defense = 10, accuracy = 4, intelligence = 0
        fighter_component = Fighter(hp = 100, strength = 4, defense = 1, accuracy = 4, intelligence = 0)
        inventory_component = Inventory(26)
        ai_component = Base_AI()

        # TODO: ADD PROPER EQUIPTMENT JESUS CHRIST
        self.equipment = {"head": None, "body": None, "l_hand": None, "r_hand": None, "arms": None, "feet": None, "l_ring": None, "r_ring": None, "ranged": None, "ammo": None}

        # Composing entity
        super().__init__(x, y, "Player", "@", "white", blocks = True, render_order = Render_Order.ACTOR, fighter = fighter_component, ai = ai_component, inventory = inventory_component)

    # Move player and adjust offset accordingly
    def move(self, dx, dy):
        self.ai.move(dx, dy)
        self.x_offset -= dx
        self.y_offset -= dy

class Goblin(Entity):
    def __init__(self, x, y):
        fighter_component = Fighter(hp = 30, strength = 3, defense = 1, accuracy = 2, intelligence = 0)
        ai_component = Basic_Monster()

        # TODO: ADD PROPER EQUIPTMENT JESUS CHRIST
        self.equipment = {"head": None, "body": None, "l_hand": None, "r_hand": None, "arms": None, "feet": None, "l_ring": None, "r_ring": None, "ranged": None, "ammo": None}

        super().__init__(x, y, "goblin", "g", "green", blocks = True, render_order = Render_Order.ACTOR, fighter = fighter_component, ai = ai_component)
