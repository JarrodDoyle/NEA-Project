import math
from components.fighter import *
from components.ai import *
from components.inventory import *
from render.render_classes import Render_Order

class Entity:
    # initialization of entity
    def __init__(self, x, y, name, char, color, blocks = False, render_order = Render_Order.CORPSE, fighter = None, ai = None, inventory = None):
        self.x = x
        self.y = y
        self.name = name
        self.char = char
        self.color = color
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        # If entity has a fighter component
        if self.fighter:
            self.fighter.owner = self
        self.ai = ai
        # If entity has an ai component
        if self.ai:
            self.ai.owner = self
        self.inventory = inventory
        # If entity has an inventory component
        if self.inventory:
            self.inventory.owner = self

    # Calculates distance between self and another entity
    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

class Player(Entity):
    # Initialization of player entity
    def __init__(self, x, y):
        # Inializing the players components
        # hp = 100, strength = 4, defense = 1, intelligence = 0
        fighter_component = Fighter(hp = 100, strength = 400, defense = 10, intelligence = 0)
        inventory_component = Inventory(26)
        ai_component = Base_AI()

        # Composing entity
        super().__init__(x, y, "Player", "@", "white", blocks = True, render_order = Render_Order.ACTOR, fighter = fighter_component, ai = ai_component, inventory = inventory_component)

    # Move player and adjust offset accordingly
    def move(self, dx, dy):
        self.ai.move(dx, dy)
        self.x_offset -= dx
        self.y_offset -= dy

class Goblin(Entity):
    def __init__(self, x, y):
        fighter_component = Fighter(hp = 30, strength = 3, defense = 0, intelligence = 0)
        ai_component = Basic_Monster()
        super().__init__(x, y, "goblin", "g", "green", blocks = True, render_order = Render_Order.ACTOR, fighter = fighter_component, ai = ai_component)
