from render.render_classes import Render_Order
from entities.entity_classes import Entity
from components.item import Item

class Health_Pot(Entity):
    def __init__(self, x, y):
        item_component = Item()
        super().__init__(x, y, "Health Pot", "!", "yellow", blocks = False, render_order = Render_Order.ITEM, item = item_component)
