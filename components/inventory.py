class Inventory:
    def __init__(self, max_items):
        self.items = []
        self.max_items = max_items

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)
