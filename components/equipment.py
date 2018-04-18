from components.component_base import Component

class Equipment(Component):
    """
    Equipment component inheriting from Component.

    Stores a dict of equipment slots and the items in those slots.
    """
    def __init__(self):
        """
        Initialize equipment component.
        """
        super().__init__()
        self.equipment = {"head": None, "body": None, "hand": None, "arms": None, "legs": None, "feet": None, "ring": None, "offhand": None, "arrows": 0}
