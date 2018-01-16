from map_generation.dungeon_base import Dungeon
from rect import Rect
import cells, random

class Dungeon_Rogue(Dungeon):
    def __init__(self, width, height):
        super().__init__(width, height)

    def split_dungeon(self):
        self.regions = []
        region_width = self.width // 3
        region_height = self.height // 3

        x, y = 0, 0

        for i in range(3):
            for j in range(3):
                region = Rect(x, y, region_width, region_height)
                self.regions.append(region)
                x += region_width
            x = 0
            y += region_height

    def gen_rooms(self):
        self.rooms = []
        for region in self.regions:
            a, b = region.get_center()
            width = random.randint(6, 14)
            height = random.randint(6, 14)
            x = a - width // 2
            y = b - height // 2
            room = Rect(x, y, width, height)
            self.rooms.append(room)
            self.dig_room([room.x1, room.x2], [room.y1, room.y2])
            

    def gen_corridors(self):
        region_width = self.width // 3
        region_height = self.height // 3

        x1, y1 = self.regions[0].get_center() # Top left region
        x2, y2 = self.regions[4].get_center() # Middle region
        x3, y3 = self.regions[8].get_center() # Bottom right region
        
        for x in range(x1, x3 + 1):
            for y in [y1, y2, y3]:
                self.tiles[y][x] = cells.Floor()        

        for y in range(y1, y3 + 1):
            for x in [x1, x2, x3]:
                self.tiles[y][x] = cells.Floor()

    def gen_dungeon(self, player):
        entity_list = []
        self.initialize_dungeon()
        self.split_dungeon()
        self.gen_rooms()
        self.gen_corridors()
        self.gen_stairs(only_in_rooms = True)
        player.x, player.y = random.choice(self.rooms).get_center()
        player.x_offset = int((2 * 17 + 46) / 2 - player.x)
        player.y_offset = int((2 * 1 + 46) / 2 - player.y)
        entity_list.append(player)
        self.gen_monsters(entity_list, only_in_rooms = True)
        self.gen_items(entity_list, only_in_rooms = True)
        return entity_list
        
