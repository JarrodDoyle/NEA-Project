import math
from render.render_classes import Render_Order

class Entity:
    # initialization of entity
    def __init__(self, x, y, name, char, color, description, blocks = False, render_order = Render_Order.CORPSE, components = {}):
        self.x = x
        self.y = y
        self.name = name
        self.char = char
        self.color = color
        self.description = description
        self.blocks = blocks
        self.render_order = render_order
        self.components = components
        for i in self.components:
            self.components.get(i).set_owner(self)

    # Calculates distance between self and another entity
    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)
