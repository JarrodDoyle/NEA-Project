from components.fighter import *
from components.ai import *
from components.inventory import *
from components.equipment import *
from components.level import *
from render.render_classes import Render_Order
from entities.entity_classes import Entity

class Player(Entity):
    # Initialization of player entity
    def __init__(self, x, y, name, fighter_class):
        # Inializing the players components
        fighter_component = Fighter(fighter_class, spawn_chance = 0)
        level_component = Level(base_level = 1, base_xp = 100, lvl_up_factor = 2)
        inventory_component = Inventory(26)
        ai_component = Base_AI()
        equipment_component = Equipment()
        components_dict = {"ai": ai_component, "inventory": inventory_component, "fighter": fighter_component, "level": level_component, "equipment": equipment_component}

        # Composing entity
        super().__init__(x, y, name, "@", "white", "This is you, the player.", blocks = True, render_order = Render_Order.ACTOR, components = components_dict)

    # Move player and adjust offset accordingly
    def move(self, dx, dy):
        self.components["ai"].move(dx, dy)
        self.x_offset -= dx
        self.y_offset -= dy

class Mob_Goblin(Entity):
    def __init__(self, x, y):
        fighter_class = Fighter_Class("goblin", strength = 3, defense = 1, accuracy = 2, intelligence = 0, dexterity = 0, max_hp = 20)
        fighter_component = Fighter(fighter_class, spawn_chance = 100)
        level_component = Level(base_level = 1, base_xp = 50, lvl_up_factor = 3, xp_drop = 2)
        ai_component = Basic_Monster()
        equipment_component = Equipment()
        components_dict = {"ai": ai_component, "fighter": fighter_component, "level": level_component, "equipment": equipment_component}
        super().__init__(x, y, "goblin", "g", "green", "An ugly green goblin.", blocks = True, render_order = Render_Order.ACTOR, components = components_dict)

class Mob_Ant(Entity):
    def __init__(self, x, y):
        fighter_class = Fighter_Class("ant", strength = 1, defense = 1, accuracy = 4, intelligence = 0, dexterity = 0, max_hp = 5)
        fighter_component = Fighter(fighter_class, spawn_chance = 100)
        level_component = Level(base_level = 1, base_xp = 50, lvl_up_factor = 3, xp_drop = 1)
        ai_component = Basic_Monster()
        equipment_component = Equipment()
        components_dict = {"ai": ai_component, "fighter": fighter_component, "level": level_component, "equipment": equipment_component}
        super().__init__(x, y, "ant", "a", "brown", "A large ant.", blocks = True, render_order = Render_Order.ACTOR, components = components_dict)

class Mob_Blob(Entity):
    def __init__(self, x, y):
        fighter_class = Fighter_Class("blob", strength = 3, defense = 2, accuracy = 2, intelligence =0, dexterity = 0, max_hp = 10)
        fighter_component = Fighter(fighter_class, spawn_chance = 100)
        level_component = Level(base_level = 1, base_xp = 50, lvl_up_factor = 3, xp_drop = 2)
        ai_component = Basic_Monster()
        equipment_component = Equipment()
        components_dict = {"ai": ai_component, "fighter": fighter_component, "level": level_component, "equipment": equipment_component}
        super().__init__(x, y, "blob", "b", "cyan", "A gooey blob.", blocks = True, render_order = Render_Order.ACTOR, components = components_dict)

class Mob_Cockatrice(Entity):
    def __init__(self, x, y):
        fighter_class = Fighter_Class("cockatrice", strength = 3, defense = 4, accuracy = 3, intelligence = 0, dexterity = 0, max_hp = 15)
        fighter_component = Fighter(fighter_class, spawn_chance = 100)
        level_component = Level(base_level = 1, base_xp = 50, lvl_up_factor = 3, xp_drop = 3)
        ai_component = Basic_Monster()
        equipment_component = Equipment()
        components_dict = {"ai": ai_component, "fighter": fighter_component, "level": level_component, "equipment": equipment_component}
        super().__init__(x, y, "cockatrice", "c", "yellow", "Dangerous bird.", blocks = True, render_order = Render_Order.ACTOR, components = components_dict)
