class Cell:
    def __init__(self, cell_name, char, bk_color = "dark gray", color = "white", is_blocked = True, blocks_sight = True):
        self.cell_name = cell_name
        self.char = char
        self.bk_color = bk_color
        self.color = color
        self.is_blocked = is_blocked
        self.blocks_sight = blocks_sight
        self.explored = False

class Wall(Cell):
    def __init__(self):
        super().__init__("wall", "▒", is_blocked = True, blocks_sight = True)

class Floor(Cell):
    def __init__(self):
        super().__init__("floor", ".", is_blocked = False, blocks_sight = False)

class Rock(Cell):
    def __init__(self):
        super().__init__("rock", "#", is_blocked = True, blocks_sight = True)
