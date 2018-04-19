from enum import Enum

class Render_Order(Enum):
    """
    Enum class for entity render orders, used to sort entities before rendering
    """
    CORPSE = 1
    ITEM = 2
    ACTOR = 3
