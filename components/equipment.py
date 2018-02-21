from components.component_base import Component

class Equipment(Component):
    def __init__(self):
        super().__init__()
        self.equipment = {"head": None, "body": None, "l_hand": None, "r_hand": None, "arms": None, "feet": None, "l_ring": None, "r_ring": None, "ranged": None, "ammo": None}



