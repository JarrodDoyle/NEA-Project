from render.render_classes import Render_Order
from entities.entity_classes import Entity
from components.item import Item
from components.weapons import Melee, Ranged, Wand
import use_functions

class Sword(Entity):
    def __init__(self, x, y):
        use_args = {"slot": "hands", "item": self}
        item_component = Item(use_function = use_functions.toggle_equip, args = use_args, spawn_chance = 100, remove_on_use = False)
        weapon_component = Melee(attack_power = 10, hits = 1)
        components_dict = {"item": item_component, "weapon": weapon_component}
        super().__init__(x, y, "Sword", "/", "cyan", "A shiny sword", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Health_Potion(Entity):
    def __init__(self, x, y):
        use_args = {"heal_amount": 30}
        item_component = Item(use_function = use_functions.heal_entity, args = use_args, spawn_chance = 100)
        components_dict = {"item": item_component}
        super().__init__(x, y, "Health Potion", "!", "yellow", "A weak health potion. Restores health to whomever drinks it.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Strength_Potion(Entity):
    def __init__(self, x, y):
        use_args = {"strength_increase": 2}
        item_component = Item(use_function = use_functions.increase_strength, args = use_args, spawn_chance = 100)
        components_dict = {"item": item_component}
        super().__init__(x, y, "Strength Potion", "!", "yellow", "A strength potion. Gives increased strength to whomever drinks it.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Defense_Potion(Entity):
    def __init__(self, x, y):
        use_args = {"defense_increase": 2}
        item_component = Item(use_function = use_functions.increase_defense, args = use_args, spawn_chance = 100)
        components_dict = {"item": item_component}
        super().__init__(x, y, "Defense Potion", "!", "yellow", "A defense potion. Gives increased defense to whomever drinks it.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Accuracy_Potion(Entity):
    def __init__(self, x, y):
        use_args = {"accuracy_increase": 2}
        item_component = Item(use_function = use_functions.increase_accuracy, args = use_args, spawn_chance = 100)
        components_dict = {"item": item_component}
        super().__init__(x, y, "Accuracy Potion", "!", "yellow", "A accuracy potion. Gives increased accuracy to whomever drinks it.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Intelligence_Potion(Entity):
    def __init__(self, x, y):
        use_args = {"intelligence_increase": 2}
        item_component = Item(use_function = use_functions.increase_intelligence, args = use_args, spawn_chance = 100)
        components_dict = {"item": item_component}
        super().__init__(x, y, "Intelligence Potion", "!", "yellow", "A intelligence potion. Gives increased intelligence to whomever drinks it.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Dexterity_Potion(Entity):
    def __init__(self, x, y):
        use_args = {"dexterity_increase": 2}
        item_component = Item(use_function = use_functions.increase_dexterity, args = use_args, spawn_chance = 100)
        components_dict = {"item": item_component}
        super().__init__(x, y, "Dexterity Potion", "!", "yellow", "A dexterity potion. Gives increased dexterity to whomever drinks it.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Max_HP_Potion(Entity):
    def __init__(self, x, y):
        use_args = {"max_hp_increase": 5}
        item_component = Item(use_function = use_functions.increase_max_hp, args = use_args, spawn_chance = 100)
        components_dict = {"item": item_component}
        super().__init__(x, y, "Max HP Potion", "!", "yellow", "A max HP potion. Gives increased max HP to whomever drinks it.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)
