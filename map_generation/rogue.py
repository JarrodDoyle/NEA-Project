from map_generation.dungeon_base import Dungeon
from rect import Rect
import cells, random

class Dungeon_Rogue(Dungeon):
    def __init__(self, width, height, rows = 3, columns = 3):
        super().__init__(width, height)
        self.rows = rows
        self.columns = columns

    def split_dungeon(self):
        self.regions = []
        region_width = self.width // self.columns
        region_height = self.height // self.rows

        x, y = 0, 0

        for i in range(self.rows):
            for j in range(self.columns):
                region = Rect(x, y, region_width, region_height)
                self.regions.append(region)
                x += region_width
            x = 0
            y += region_height

    def gen_rooms(self):
        self.rooms = []
        for region in self.regions:
            a, b = region.get_center()
            width = random.randint((region.x2 - region.x1) // 4, (region.x2- region.x1) // 2)
            height = random.randint((region.y2 - region.y1) // 4, (region.y2 - region.y1) // 2)
            x = a - width // 2
            y = b - height // 2
            room = Rect(x, y, width, height)
            self.rooms.append(room)
            self.dig_room([room.x1, room.x2], [room.y1, room.y2])
            

    def gen_corridors(self):
        region_width = self.width // self.columns
        region_height = self.height // self.rows

        x_vals = []
        y_vals = []
        for i in range(0, self.columns):
            x_vals.append(self.regions[i].get_center()[0])

        for i in range(0, self.rows):
            y_vals.append(self.regions[i*self.columns].get_center()[1])
        
        for x in range(min(x_vals), max(x_vals) + 1):
            for y in y_vals:
                self.tiles[y][x] = cells.Floor()        

        for y in range(min(y_vals), max(y_vals)):
            for x in x_vals:
                self.tiles[y][x] = cells.Floor()

    def gen_dungeon(self, player):
        self.initialize_dungeon()
        self.split_dungeon()
        self.gen_rooms()
        self.gen_corridors()
        self.gen_stairs(only_in_rooms = True)
        self.set_player_coords(player)
        entity_list = [player]
        self.gen_monsters(player, entity_list, only_in_rooms = True)
        self.gen_items(entity_list, only_in_rooms = True)
        return entity_list
        
