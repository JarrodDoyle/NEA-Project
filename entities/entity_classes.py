import math
from render.render_classes import Render_Order

class Entity:
    """
    Entity class to be used by all entities.
    """
    def __init__(self, x, y, name, char, color, description, blocks = False, render_order = Render_Order.CORPSE, components = {}):
        """
        Initialize entity

        x -- starting x coordinate
        y -- starting y coordinate
        name -- entity name
        char -- character used to represent entity within the world
        color -- color of all entity representations
        description -- short description of the entity
        blocks -- boolean value for whetyher the entity blocks movement (default to False)
        render_order -- enum used to sort entities for rendering
        components -- dictionary containing all entity components
        """
        self.x = x
        self.y = y
        self.name = name
        self.char = char
        self.color = color
        self.description = description
        self.blocks = blocks
        self.render_order = render_order
        self.components = components
        # Sets the owner of each component to self
        for i in self.components:
            self.components.get(i).set_owner(self)

    def distance_to(self, other):
        """
        Return the distance between self and another entity
        """
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)
