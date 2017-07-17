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
