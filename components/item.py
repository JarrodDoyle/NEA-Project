from components.component_base import Component
import use_functions

class Item(Component):
    def __init__(self, use_function, args, remove_on_use = True):
        self.use_function = use_function
        self.args = args
        self.remove_on_use = remove_on_use
        super().__init__()

    def use(self, entity, inventory):
        results = []
        used = self.use_function(entity, self.args)
        if used:
            results.append({"message": "You used the {}.".format(self.owner.name)})
            if self.remove_on_use:
                inventory.remove_item(self.owner)
        else:
            results.append({"message": "You failed to use the {}.".format(self.owner.name)})
        return results

    def drop(self, entity_list, entity, inventory):
        results = []
        inventory.remove_item(self.owner)
        self.owner.x = entity.x
        self.owner.y = entity.y
        entity_list.append(self.owner)
        if self.use_function == use_functions.toggle_equip:
            results.extend(self.use(entity, inventory))
        results.append({"message": "You drop the {} on the ground.".format(self.owner.name)})
        return results
