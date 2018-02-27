from components.component_base import Component

class Equipment(Component):
    def __init__(self):
        super().__init__()
        self.equipment = {"head": None, "body": None, "hand": None, "arms": None, "legs": None, "feet": None, "ring": None, "offhand": None, "arrows": 0}
