from map_generation.dungeon_base import Dungeon
from rect import Rect
import cells, random

class Dungeon_Rogue(Dungeon):
    """
    Class used to generate dungeons similar to those found in "Rogue"
    """
    def __init__(self, width, height, rows = 3, columns = 3):
        """
        Initialize rogue dungeon

        width -- dungeon width
        height -- dungeon height
        rows -- how many rows of rooms should occur
        columns -- how many columns of rooms should occur
        """
        super().__init__(width, height)
        self.rows = rows
        self.columns = columns

    def split_dungeon(self):
        """
        Split dungeon into room regions

        Create a list of regions where rooms can spawn, regions are represented
        using Rect's
        """
        self.regions = []

        region_width = self.width // self.columns
        region_height = self.height // self.rows

        # Starting from the top left corner of the dungeon
        x, y = 0, 0

        # For each row or rooms
        for i in range(self.rows):
            # For each room in the row
            for j in range(self.columns):
                region = Rect(x, y, region_width, region_height)
                self.regions.append(region)
                x += region_width
            # Reset x position
            x = 0
            y += region_height

    def gen_rooms(self):
        """
        Generate rooms inside previously generated regions

        All rooms center on the region center to allow for easy room connection.
        """
        self.rooms = []
        for region in self.regions:
            # Room center == region center
            a, b = region.get_center()
            # Width/height between 1/2 and 1/4 of the respective region attribute
            width = random.randint((region.x2 - region.x1) // 4, (region.x2- region.x1) // 2)
            height = random.randint((region.y2 - region.y1) // 4, (region.y2 - region.y1) // 2)
            # Top left corner of room Rect
            x = a - width // 2
            y = b - height // 2
            room = Rect(x, y, width, height)
            # Add to rooms list and dig the room
            self.rooms.append(room)
            self.dig_room([room.x1, room.x2], [room.y1, room.y2])


    def gen_corridors(self):
        """
        Generate corridors between rooms
        """
        region_width = self.width // self.columns
        region_height = self.height // self.rows

        x_vals = []
        y_vals = []

        # Get the x coordinates of each room center
        for i in range(0, self.columns):
            x_vals.append(self.regions[i].get_center()[0])

        # Get the y coordinates of each room center
        for i in range(0, self.rows):
            y_vals.append(self.regions[i*self.columns].get_center()[1])

        # Draw all horizontal corridors
        for x in range(min(x_vals), max(x_vals) + 1):
            for y in y_vals: # For each row
                self.tiles[y][x] = cells.Floor()

        # Draw all vertical corridors
        for y in range(min(y_vals), max(y_vals)):
            for x in x_vals: # For each column
                self.tiles[y][x] = cells.Floor()

    def gen_dungeon(self, player, floor_index):
        """
        Generate full "rogue dungeon" and return the entities in it
        """
        self.initialize_dungeon()
        self.split_dungeon()
        self.gen_rooms()
        self.gen_corridors()
        self.gen_stairs(only_in_rooms = True)
        self.set_player_coords(player)
        entity_list = [player]
        self.gen_monsters(player, entity_list, floor_index, only_in_rooms = True)
        self.gen_items(entity_list, floor_index, only_in_rooms = True)
        return entity_list
