import libtcodpy as libtcod

class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def get_center(self):
        x = (self.x1 + self.x2) // 2
        y = (self.y1 + self.y2) // 2
        return x, y

    def get_area(self):
        width = self.x2 - self.x1
        height = self.y2 - self.y1
        return int(width * height)

class BSPTree:
    def __init__(self, width, height):
        self.map_width = width
        self.map_height = height

    def gen_blank(self):
        self.level = [["#" for x in range(self.map_width)] for y in range(self.map_height)]

    def gen_level(self):
        self.gen_blank()
        root_leaf = Leaf(0, 0, self.map_width, self.map_height)
        self.leaves = [root_leaf]

class Leaf:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.child_l = None
        self.child_r = None
        self.room = None
        self.hall = None
