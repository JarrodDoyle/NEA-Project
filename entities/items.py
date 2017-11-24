from render.render_classes import Render_Order
from entities.entity_classes import Entity
from components.item import Item
import use_functions

class Health_Pot(Entity):
    def __init__(self, x, y):
        item_component = Item(use_function = use_functions.heal_entity, args = [30])
        components_dict = {"item": item_component}
        super().__init__(x, y, "Health Pot", "!", "yellow", "A weak health potion. Restores health to whomever drinks it.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)
