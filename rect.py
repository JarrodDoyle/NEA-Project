class Rect:
    """
    Class representing a rectangle
    """
    def __init__(self, x, y, w, h):
        """
        Initialize rectangle object

        x -- x coordinate of the top left corner of rectangle
        y -- y coordinate of the top left corner of rectangle
        w -- width of the rectangle
        h -- height of the rectangle
        """
        # Top left corner
        self.x1 = x
        self.y1 = y
        # Bottom right corner
        self.x2 = x + w - 1
        self.y2 = y + h - 1

    def get_center(self):
        """
        Return the center x/y of the rectangle
        """
        # Floor to ensure integer values in rects with odd width/height
        x = (self.x1 + self.x2) // 2
        y = (self.y1 + self.y2) // 2
        return x, y

    def get_area(self):
        """
        Return the area of the rectangle
        """
        width = self.x2 - self.x1
        height = self.y2 - self.y1
        return int(width * height)
