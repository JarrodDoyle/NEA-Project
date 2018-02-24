from components.component_base import Component
import use_functions

class Item(Component):
    def __init__(self, use_function, args, spawn_chance, remove_on_use = True):
        self.use_function = use_function
        self.spawn_chance = spawn_chance
        self.args = args
        self.remove_on_use = remove_on_use
        super().__init__()

    def use(self, entity, inventory):
        used = self.use_function(entity, self.args)
        if used:
            message = "You used the {}.".format(self.owner.name)
            if self.remove_on_use:
                inventory.remove_item(self.owner)
        else:
            message = "You failed to use the {}.".format(self.owner.name)
        return message

    def drop(self, entity_list, entity, inventory):
        inventory.items.remove(self.owner)
        self.owner.x = entity.x
        self.owner.y = entity.y
        entity_list.append(self.owner)
        if self.use_function == use_functions.toggle_equip:
            self.use(entity, inventory)
