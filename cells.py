class Cell:
    def __init__(self, cell_name, char, bk_color = "dark gray", color = "white", is_blocked = True, blocks_sight = True):
        self.cell_name = cell_name
        self.base_char = char
        self.base_bk_color = bk_color
        self.base_color = color
        self.is_blocked = is_blocked
        self.blocks_sight = blocks_sight
        self.item = None
        self.entity = None
        self.explored = False

    def add_entity(self, entity):
        self.entity = entity

    def remove_entity(self):
        self.entity = None

    def add_item(self,  item):
        self.item = item

    def remove_item(self):
        self.item = None

    @property
    def char(self):
        if self.entity:
            return self.entity.char
        if self.item:
            return self.item.char
        return self.base_char

    @property
    def color(self):
        if self.entity:
            return self.entity.color
        if self.item:
            return self.item.color
        return self.base_color

    @property
    def bk_color(self):
        if self.entity:
            return self.entity.color
        if self.item:
            return self.item.color
        return self.base_bk_color

class Wall(Cell):
    def __init__(self):
        super().__init__("wall", "▒", is_blocked = True, blocks_sight = True)

class Floor(Cell):
    def __init__(self):
        super().__init__("floor", ".", is_blocked = False, blocks_sight = False)

class Rock(Cell):
    def __init__(self):
        super().__init__("rock", "#", is_blocked = True, blocks_sight = True)
