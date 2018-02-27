from render.render_classes import Render_Order
from entities.entity_classes import Entity
from components.item import Item
from components.weapons import Melee, Ranged, Wand
from components.armor import Armor
import use_functions

class Leather_Helmet(Entity):
    base_spawn_weight = 10
    lowest_level_spawn = 0
    def __init__(self, x, y):
        use_args = {"slot": "head", "item": self}
        item_component = Item(use_function = use_functions.toggle_equip, args = use_args, remove_on_use = False)
        armor_component = Armor(bonus_stats = {"defense": 1})
        components_dict = {"item": item_component, "armor": armor_component}
        super().__init__(x, y, "Leather Helmet", "~", "brown", "A leather helmet.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Leather_Chestplate(Entity):
    base_spawn_weight = 10
    lowest_level_spawn = 0
    def __init__(self, x, y):
        use_args = {"slot": "body", "item": self}
        item_component = Item(use_function = use_functions.toggle_equip, args = use_args, remove_on_use = False)
        armor_component = Armor(bonus_stats = {"defense": 1})
        components_dict = {"item": item_component, "armor": armor_component}
        super().__init__(x, y, "Leather Chestplate", "~", "brown", "A leather Chestplate.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Leather_Bracers(Entity):
    base_spawn_weight = 10
    lowest_level_spawn = 0
    def __init__(self, x, y):
        use_args = {"slot": "arms", "item": self}
        item_component = Item(use_function = use_functions.toggle_equip, args = use_args, remove_on_use = False)
        armor_component = Armor(bonus_stats = {"defense": 1})
        components_dict = {"item": item_component, "armor": armor_component}
        super().__init__(x, y, "Leather Bracers", "~", "brown", "Some leather bracers.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Leather_Greaves(Entity):
    base_spawn_weight = 10
    lowest_level_spawn = 0
    def __init__(self, x, y):
        use_args = {"slot": "legs", "item": self}
        item_component = Item(use_function = use_functions.toggle_equip, args = use_args, remove_on_use = False)
        armor_component = Armor(bonus_stats = {"defense": 1})
        components_dict = {"item": item_component, "armor": armor_component}
        super().__init__(x, y, "Leather Greaves", "~", "brown", "Some leather greaves.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Leather_Boots(Entity):
    base_spawn_weight = 10
    lowest_level_spawn = 0
    def __init__(self, x, y):
        use_args = {"slot": "feet", "item": self}
        item_component = Item(use_function = use_functions.toggle_equip, args = use_args, remove_on_use = False)
        armor_component = Armor(bonus_stats = {"defense": 1})
        components_dict = {"item": item_component, "armor": armor_component}
        super().__init__(x, y, "Leather Boots", "~", "brown", "Some leather boots.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Intelligence_Ring(Entity):
    base_spawn_weight = 10
    lowest_level_spawn = 0
    def __init__(self, x, y):
        use_args = {"slot": "ring", "item": self}
        item_component = Item(use_function = use_functions.toggle_equip, args = use_args, remove_on_use = False)
        armor_component = Armor(bonus_stats = {"intelligence": 2})
        components_dict = {"item": item_component, "armor": armor_component}
        super().__init__(x, y, "Ring of Intelligence", "=", "cyan", "An enchanted ring. Increases intelligence while worn.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Accuracy_Ring(Entity):
    base_spawn_weight = 10
    lowest_level_spawn = 0
    def __init__(self, x, y):
        use_args = {"slot": "ring", "item": self}
        item_component = Item(use_function = use_functions.toggle_equip, args = use_args, remove_on_use = False)
        armor_component = Armor(bonus_stats = {"accuracy": 2})
        components_dict = {"item": item_component, "armor": armor_component}
        super().__init__(x, y, "Ring of Accuracy", "=", "cyan", "An enchanted ring. Increases accuracy while worn.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Strength_Ring(Entity):
    base_spawn_weight = 10
    lowest_level_spawn = 0
    def __init__(self, x, y):
        use_args = {"slot": "ring", "item": self}
        item_component = Item(use_function = use_functions.toggle_equip, args = use_args, remove_on_use = False)
        armor_component = Armor(bonus_stats = {"strength": 2})
        components_dict = {"item": item_component, "armor": armor_component}
        super().__init__(x, y, "Ring of Strength", "=", "cyan", "An enchanted ring. Increases strength while worn.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Dexterity_Ring(Entity):
    base_spawn_weight = 10
    lowest_level_spawn = 0
    def __init__(self, x, y):
        use_args = {"slot": "ring", "item": self}
        item_component = Item(use_function = use_functions.toggle_equip, args = use_args, remove_on_use = False)
        armor_component = Armor(bonus_stats = {"dexterity": 2})
        components_dict = {"item": item_component, "armor": armor_component}
        super().__init__(x, y, "Ring of Dexterity", "=", "cyan", "An enchanted ring. Increases dexterity while worn.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Weak_Food(Entity):
    base_spawn_weight = 10
    lowest_level_spawn = 0
    def __init__(self, x, y):
        use_args = {"hunger_decrease_ratio": 0.5}
        item_component = Item(use_function = use_functions.decrease_hunger, args = use_args)
        components_dict = {"item": item_component}
        super().__init__(x, y, "Weak Food", "%", "brown", "A moderately filling piece of food.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Strong_Food(Entity):
    base_spawn_weight = 5
    lowest_level_spawn = 0
    def __init__(self, x, y):
        use_args = {"hunger_decrease_ratio": 1}
        item_component = Item(use_function = use_functions.decrease_hunger, args = use_args)
        components_dict = {"item": item_component}
        super().__init__(x, y, "Food", "%", "brown", "A filling piece of food.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Test_Wand(Entity):
    base_spawn_weight = 15
    lowest_level_spawn = 0
    def __init__(self, x, y):
        use_args = {"slot": "offhand", "item": self}
        item_component = Item(use_function = use_functions.toggle_equip, args = use_args, remove_on_use = False)
        weapon_component = Wand(attack_power = 40, attack_range = 5, hits = 1, charges = 1)
        components_dict = {"item": item_component, "weapon": weapon_component}
        super().__init__(x, y, "TEST WAND", ")", "red", "A test wand.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Iron_Sword(Entity):
    base_spawn_weight = 10
    lowest_level_spawn = 8
    def __init__(self, x, y):
        use_args = {"slot": "hand", "item": self}
        item_component = Item(use_function = use_functions.toggle_equip, args = use_args, remove_on_use = False)
        weapon_component = Melee(attack_power = 10, attack_range = 1, hits = 1)
        components_dict = {"item": item_component, "weapon": weapon_component}
        super().__init__(x, y, "Iron Sword", ")", "cyan", "A shiny sword.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Copper_Sword(Entity):
    base_spawn_weight = 15
    lowest_level_spawn = 5
    def __init__(self, x, y):
        use_args = {"slot": "hand", "item": self}
        item_component = Item(use_function = use_functions.toggle_equip, args = use_args, remove_on_use = False)
        weapon_component = Melee(attack_power = 5, attack_range = 1, hits = 1)
        components_dict = {"item": item_component, "weapon": weapon_component}
        super().__init__(x, y, "Copper Sword", ")", "orange", "A copper sword.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Copper_Dagger(Entity):
    base_spawn_weight = 10
    lowest_level_spawn = 0
    def __init__(self, x, y):
        use_args = {"slot": "hand", "item": self}
        item_component = Item(use_function = use_functions.toggle_equip, args = use_args, remove_on_use = False)
        weapon_component = Melee(attack_power = 2, attack_range = 1, hits = 1)
        components_dict = {"item": item_component, "weapon": weapon_component}
        super().__init__(x, y, "Copper Dagger", ")", "orange", "A short copper dagger.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Iron_Dagger(Entity):
    base_spawn_weight = 15
    lowest_level_spawn = 3
    def __init__(self, x, y):
        use_args = {"slot": "hand", "item": self}
        item_component = Item(use_function = use_functions.toggle_equip, args = use_args, remove_on_use = False)
        weapon_component = Melee(attack_power = 4, attack_range = 1, hits = 1)
        components_dict = {"item": item_component, "weapon": weapon_component}
        super().__init__(x, y, "Iron Dagger", ")", "cyan", "A short iron dagger.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Copper_Axe(Entity):
    base_spawn_weight = 15
    lowest_level_spawn = 3
    def __init__(self, x, y):
        use_args = {"slot": "hand", "item": self}
        item_component = Item(use_function = use_functions.toggle_equip, args = use_args, remove_on_use = False)
        weapon_component = Melee(attack_power = 4, attack_range = 1, hits = 1)
        components_dict = {"item": item_component, "weapon": weapon_component}
        super().__init__(x, y, "Copper Axe", ")", "orange", "A copper axe.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Iron_Axe(Entity):
    base_spawn_weight = 10
    lowest_level_spawn = 6
    def __init__(self, x, y):
        use_args = {"slot": "hand", "item": self}
        item_component = Item(use_function = use_functions.toggle_equip, args = use_args, remove_on_use = False)
        weapon_component = Melee(attack_power = 8, attack_range = 1, hits = 1)
        components_dict = {"item": item_component, "weapon": weapon_component}
        super().__init__(x, y, "Iron Axe", ")", "cyan", "An iron axe.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Battle_Axe(Entity):
    base_spawn_weight = 5
    lowest_level_spawn = 6
    def __init__(self, x, y):
        use_args = {"slot": "hand", "item": self}
        item_component = Item(use_function = use_functions.toggle_equip, args = use_args, remove_on_use = False)
        weapon_component = Melee(attack_power = 12, attack_range = 1, hits = 1)
        components_dict = {"item": item_component, "weapon": weapon_component}
        super().__init__(x, y, "Battle Axe", ")", "yellow", "A large battle axe.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Copper_Longsword(Entity):
    base_spawn_weight = 15
    lowest_level_spawn = 8
    def __init__(self, x, y):
        use_args = {"slot": "hand", "item": self}
        item_component = Item(use_function = use_functions.toggle_equip, args = use_args, remove_on_use = False)
        weapon_component = Melee(attack_power = 7, attack_range = 1, hits = 1)
        components_dict = {"item": item_component, "weapon": weapon_component}
        super().__init__(x, y, "Copper Longsword", ")", "orange", "A large copper sword.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Iron_Longsword(Entity):
    base_spawn_weight = 10
    lowest_level_spawn = 10
    def __init__(self, x, y):
        use_args = {"slot": "hand", "item": self}
        item_component = Item(use_function = use_functions.toggle_equip, args = use_args, remove_on_use = False)
        weapon_component = Melee(attack_power = 14, attack_range = 1, hits = 1)
        components_dict = {"item": item_component, "weapon": weapon_component}
        super().__init__(x, y, "Iron Longsword", ")", "cyan", "A large iron sword.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Health_Potion(Entity):
    base_spawn_weight = 5
    lowest_level_spawn = 0
    def __init__(self, x, y):
        use_args = {"heal_amount": 30}
        item_component = Item(use_function = use_functions.heal_entity, args = use_args)
        components_dict = {"item": item_component}
        super().__init__(x, y, "Health Potion", "!", "yellow", "A weak health potion. Restores health to whomever drinks it.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Strength_Potion(Entity):
    base_spawn_weight = 5
    lowest_level_spawn = 0
    def __init__(self, x, y):
        use_args = {"strength_increase": 2}
        item_component = Item(use_function = use_functions.increase_strength, args = use_args)
        components_dict = {"item": item_component}
        super().__init__(x, y, "Strength Potion", "!", "yellow", "A strength potion. Gives increased strength to whomever drinks it.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Defense_Potion(Entity):
    base_spawn_weight = 5
    lowest_level_spawn = 0
    def __init__(self, x, y):
        use_args = {"defense_increase": 2}
        item_component = Item(use_function = use_functions.increase_defense, args = use_args)
        components_dict = {"item": item_component}
        super().__init__(x, y, "Defense Potion", "!", "yellow", "A defense potion. Gives increased defense to whomever drinks it.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Accuracy_Potion(Entity):
    base_spawn_weight = 5
    lowest_level_spawn = 0
    def __init__(self, x, y):
        use_args = {"accuracy_increase": 2}
        item_component = Item(use_function = use_functions.increase_accuracy, args = use_args)
        components_dict = {"item": item_component}
        super().__init__(x, y, "Accuracy Potion", "!", "yellow", "A accuracy potion. Gives increased accuracy to whomever drinks it.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Intelligence_Potion(Entity):
    base_spawn_weight = 5
    lowest_level_spawn = 0
    def __init__(self, x, y):
        use_args = {"intelligence_increase": 2}
        item_component = Item(use_function = use_functions.increase_intelligence, args = use_args)
        components_dict = {"item": item_component}
        super().__init__(x, y, "Intelligence Potion", "!", "yellow", "A intelligence potion. Gives increased intelligence to whomever drinks it.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Dexterity_Potion(Entity):
    base_spawn_weight = 5
    lowest_level_spawn = 0
    def __init__(self, x, y):
        use_args = {"dexterity_increase": 2}
        item_component = Item(use_function = use_functions.increase_dexterity, args = use_args)
        components_dict = {"item": item_component}
        super().__init__(x, y, "Dexterity Potion", "!", "yellow", "A dexterity potion. Gives increased dexterity to whomever drinks it.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)

class Max_HP_Potion(Entity):
    base_spawn_weight = 5
    lowest_level_spawn = 4
    def __init__(self, x, y):
        use_args = {"max_hp_increase": 5}
        item_component = Item(use_function = use_functions.increase_max_hp, args = use_args)
        components_dict = {"item": item_component}
        super().__init__(x, y, "Max HP Potion", "!", "yellow", "A max HP potion. Gives increased max HP to whomever drinks it.", blocks = False, render_order = Render_Order.ITEM, components = components_dict)
