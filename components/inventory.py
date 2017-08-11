import libtcodpy as libtcod

class Inventory:
    def __init__(self, max_items):
        self.items = []
        self.max_items = max_items

    def add_item(self, item):
        results = []
        if len(self.items) >= self.max_items:
            results.append({"item_added": None, "message": "[color=yellow]You cannot carry any more, your inventory is full."})
        else:
            results.append({"item_added": item, "message": "[color=blue]You pick up the {}!".format(item.name)})
            self.items.append(item)
        return results

    def remove_item(self, item):
        self.items.remove(item)
