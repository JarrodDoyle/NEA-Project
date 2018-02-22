from components.component_base import Component


class Item(Component):
    def __init__(self, use_function, args, spawn_chance):
        self.use_function = use_function
        self.spawn_chance = spawn_chance
        self.args = args
        super().__init__()

    def use(self, entity, inventory):
        used = self.use_function(entity, self.args)
        if used:
            message = "You used the {}.".format(self.owner.name)
            inventory.remove_item(self.owner)
        else:
            message = "You failed to use the {}.".format(self.owner.name)
        return message
