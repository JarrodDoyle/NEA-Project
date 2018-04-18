from components.component_base import Component
import use_functions

class Item(Component):
    """
    Item component inheriting from Component
    """
    def __init__(self, use_function, args, remove_on_use = True):
        """
        Initialize item component.

        use_function -- function to be called when the item is used
        args -- dictionary containing the arguments use_function will use
        remove_on_use -- boolean value for whether to remove the item from
        inventory after using it
        """
        self.use_function = use_function
        self.args = args
        self.remove_on_use = remove_on_use
        super().__init__()

    def use(self, entity, inventory):
        """
        Attempt to use an item and return the results.

        entity -- the item to be used
        inventory -- inventory to remove from if remove_on_use is true
        """
        results = []
        used = self.use_function(entity, self.args) # Use function returns whether the use was successful
        if used:
            results.append({"message": "You used the {}.".format(self.owner.name)})
            if self.remove_on_use:
                inventory.remove_item(self.owner)
        else:
            results.append({"message": "You failed to use the {}.".format(self.owner.name)})
        return results

    def drop(self, entity_list, entity, inventory):
        """
        Return the results of dropping an item on the floor.

        entity_list -- list of entity on the dungeon floor
        entity -- the item being dropped
        inventory -- the inventory the item is being removed from
        """
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
