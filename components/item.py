from components.component_base import Component
import use_functions

class Item(Component):
    def __init__(self, use_function, args, remove_on_use = True): # Where args is a dict
        self.use_function = use_function
        self.args = args
        self.remove_on_use = remove_on_use
        super().__init__()

    # Attempts to use the item
    def use(self, entity, inventory):
        results = []
        used = self.use_function(entity, self.args) # Use function returns whether the use was successful
        if used:
            results.append({"message": "You used the {}.".format(self.owner.name)})
            if self.remove_on_use:
                inventory.remove_item(self.owner)
        else:
            results.append({"message": "You failed to use the {}.".format(self.owner.name)})
        return results

    # Drops item on dungeon floor
    def drop(self, entity_list, entity, inventory):
        results = []
        inventory.remove_item(self.owner)
        # Set the x and y coordinates of the item to the x and y of the entity holding it
        self.owner.x = entity.x
        self.owner.y = entity.y
        entity_list.append(self.owner) # Add the item to the list of entities in the dungeon
        # If the item is an equippable attempt to dequip it
        if self.use_function == use_functions.toggle_equip:
            equipment_component = entity.components.get("equipment")
            slot = self.args.get("slot")
            item = self.args.get("item")
            use_functions.dequip(equipment_component.equipment, slot, item)
        results.append({"message": "You drop the {} on the ground.".format(self.owner.name)})
        return results
