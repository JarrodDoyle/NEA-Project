import math
from render.render_classes import Render_Order

class Entity:
    # initialization of entity
    def __init__(self, x, y, name, char, color, blocks = False, render_order = Render_Order.CORPSE, fighter = None, ai = None, inventory = None, item = None):
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
        self.item = item
        if self.item:
            self.item.owner = self

    # Calculates distance between self and another entity
    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)
