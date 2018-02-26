import libtcodpy as libtcod
from components.component_base import Component

class Inventory(Component):
    def __init__(self, max_items):
        super().__init__()
        self.items = {"num_items": 0}
        self.max_items = max_items

    def add_item(self, item):
        results = []
        if self.items["num_items"] >= self.max_items:
            results.append({"item_added": None, "message": "[color=yellow]You cannot carry any more, your inventory is full."})
        else:
            results.append({"item_added": item, "message": "[color=light blue]You pick up the {}!".format(item.name)})
            self.items["num_items"] += 1
            if self.items.get(item.name) is not None:
                self.items[item.name].append(item)
            else:
                self.items[item.name] = [item]
        return results

    def remove_item(self, item):
        self.items[item.name].remove(item)
        if self.items[item.name] == []:
            del self.items[item.name]
        self.items["num_items"] -= 1
