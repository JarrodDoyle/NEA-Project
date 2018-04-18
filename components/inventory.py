import libtcodpy as libtcod
from components.component_base import Component

class Inventory(Component):
    """
    Inventory component inheriting from Component
    """
    def __init__(self, max_items):
        """
        Initialize inventory component

        max_items -- Maximum amount of items that can be in the inventory
        """
        super().__init__()
        self.items = {"num_items": 0}
        self.max_items = max_items

    def add_item(self, item):
        """
        Attempt to add item to inventory and return the results.
        """
        results = []
        # If inventory is full
        if self.items["num_items"] >= self.max_items:
            results.append({"item_added": None, "message": "[color=yellow]You cannot carry any more, your inventory is full."})
        else:
            results.append({"item_added": item, "message": "[color=light blue]You pick up the {}!".format(item.name)})
            self.items["num_items"] += 1
            # If an item of this type is already in the inventory add it to the list of the item type
            if self.items.get(item.name) is not None:
                self.items[item.name].append(item)
            # Otherwise create a new key with a list of the item
            else:
                self.items[item.name] = [item]
        return results

    def remove_item(self, item):
        """
        Attempt to remove item from inventory and return the results.
        """
        self.items[item.name].remove(item)
        # If there are no longer any items of the item type in inventory, delete the key from the items dict
        if self.items[item.name] == []:
            del self.items[item.name]
        self.items["num_items"] -= 1
