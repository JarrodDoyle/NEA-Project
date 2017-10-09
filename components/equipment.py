from components.component_base import Component

class Equipment(component):
    def __init__(self):
        super().__init__()
        self.equipment = {}

    def equip_item(self, item, slot):
        if self.equipment[slot] == None:
            self.equipment[slot] = item


