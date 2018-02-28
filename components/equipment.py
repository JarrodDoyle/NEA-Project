from components.component_base import Component

class Equipment(Component):
    # Component for equipment. Has a dict with all equipment slots and whats held in those slots.
    def __init__(self):
        super().__init__()
        self.equipment = {"head": None, "body": None, "hand": None, "arms": None, "legs": None, "feet": None, "ring": None, "offhand": None, "arrows": 0}
