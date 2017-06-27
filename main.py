import libtcodpy as libtcod
import math, textwrap

SCREENWIDTH = 80
SCREENHEIGHT = 50
MAPWIDTH = 80
MAPHEIGHT = 43
ROOMMAXSIZE = 10
ROOMMINSIZE = 6
MAXROOMS = 30
MAX_ROOM_MONSTERS = 3
LIMITFPS = 20
BAR_WIDTH = 20
PANELHEIGHT = 7
PANEL_Y = SCREENHEIGHT - PANELHEIGHT
MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREENWIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANELHEIGHT - 1
MAX_ROOM_ITEMS = 2
INVENTORY_WIDTH = 50
HEAL_AMOUNT = 4
LIGHTNING_DAMAGE = 20
LIGHTNING_RANGE = 5

FOV_ALGO = 0
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

color_dark_wall = libtcod.Color(0, 0, 100)
color_light_wall = libtcod.Color(130, 110, 50)
color_dark_ground = libtcod.Color(50, 50, 150)
color_light_ground = libtcod.Color(200, 180, 50)

class Item:
    def __init__(self, use_function = None):
        self.use_function = use_function

    def pick_up(self):
        if len(inventory) >= 26:
            message("Your inventory is full cannot pick up {}.".format(self.owner.name), libtcod.red)
        else:
            inventory.append(self.owner)
            objects.remove(self.owner)
            message("You picked up a {} !".format(self.owner.name), libtcod.green)

    def use(self):
        if self.use_function == None:
            message("The {} cannot be used.".format(self.owner.name))
        else:
            if self.use_function() != "cancelled":
                inventory.remove(self.owner)

class Fighter:
    def __init__(self, hp, defense, power, death_function = None):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.death_function = death_function

    def take_damage(self, damage):
        if damage > 0:
            self.hp -= damage
            if self.hp <= 0:
                function = self.death_function
                if function != None:
                    function(self.owner)

    def attack(self, target):
        damage = self.power - target.fighter.defense
        if damage > 0:
            message("{} attacks {} for {} hit points".format(self.owner.name.capitalize(), target.name, damage))
            target.fighter.take_damage(damage)
        else:
            message("{} attacks {} but it has no effect!.".format(self.owner.name.capitalize(), target.name))

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

class BasicMonster:
    def take_turn(self):
        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            if monster.distance_to(player) >= 2:
                monster.move_towards(player.x, player.y)
            elif player.fighter.hp > 0:
                monster.fighter.attack(player)

class Object:
    def __init__(self, x, y, char, name, color, blocks = False, fighter = None, ai = None, item = None):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.blocks = blocks
        self.fighter = fighter
        if self.fighter:
            self.fighter.owner = self
        self.ai = ai
        if self.ai:
            self.ai.owner = self
        self.item = item
        if self.item:
            self.item.owner = self

    def send_to_back(self):
        global objects
        objects.remove(self)
        objects.insert(0, self)

    def move(self, dx, dy):
        if not is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        temp_dx = dx
        temp_dy = dy

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        if temp_dx > 0 and dx == 0:
            dx = 1
        elif temp_dx < 0 and dx == 0:
            dx = -1
        if temp_dy > 0 and dy == 0:
            dy = 1
        elif temp_dy < 0 and dy == 0:
            dy = -1

        self.move(dx, dy)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def draw(self):
        if libtcod.map_is_in_fov(fov_map, self.x, self.y):
            libtcod.console_set_default_foreground(con, self.color)
            libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def clear(self):
        libtcod.console_put_char(con, self.x, self.y, " ", libtcod.BKGND_NONE)

class Tile:
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
        if block_sight == None:
            block_sight = blocked
        self.block_sight = block_sight
        self.explored = False

class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def get_center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return center_x, center_y

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1)

def closest_monster(max_range):
    closest_enemy = None
    closest_dist = max_range + 1

    for obj in objects:
        if obj.fighter and obj != player and libtcod.map_is_in_fov(fov_map, obj.x, obj.y):
            dist = player.distance_to(obj)
            if dist < closest_dist:
                closest_enemy = obj
                closest_dist = dist
    return closest_enemy

def player_death(player):
    global game_state
    message("You died!", libtcod.red)
    game_state = "dead"
    player.char = "%"
    player.color = libtcod.dark_red

def monster_death(monster):
    message("{} is dead!".format(monster.name.capitalize()), libtcod.orange)
    monster.char = "%"
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = "remains of {}.".format(monster.name)
    monster.send_to_back()

def is_blocked(x, y):
    if map[x][y].blocked:
        return True

    for obj in objects:
        if obj.blocks and obj.x == x and obj.y == y:
            return True
    return False

def place_objects(room):
    num_monsters = libtcod.random_get_int(0, 1, MAX_ROOM_MONSTERS)

    for i in range(num_monsters):
        x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
        y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)

        if not is_blocked(x, y):
            if libtcod.random_get_int(0, 0, 100) < 80:
                fighter_component = Fighter(10, 0, 3, death_function = monster_death)
                ai_component = BasicMonster()
                monster = Object(x, y, "O", "orc", libtcod.desaturated_green, blocks = True, fighter = fighter_component, ai = ai_component)
            else:
                fighter_component = Fighter(16, 1, 4, death_function = monster_death)
                ai_component = BasicMonster()
                monster = Object(x, y, "T", "troll", libtcod.darker_green, blocks = True, fighter = fighter_component, ai = ai_component)

            objects.append(monster)

    num_items = libtcod.random_get_int(0, 0, MAX_ROOM_ITEMS)

    for i in range(num_items):
        x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
        y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)

        if not is_blocked(x, y):
            if libtcod.random_get_int(0, 0, 100) < 70:
                item_component = Item(use_function = cast_heal)
                item = Object(x, y, "!", "healing potion", libtcod.violet, item = item_component)
            else:
                item_component = Item(use_function = cast_lightning)
                item = Object(x, y, "#", "scroll of lightning bolt", libtcod.light_yellow, item = item_component)
            objects.append(item)
            item.send_to_back()

def create_room(room):
    global map

    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            map[x][y].blocked = False
            map[x][y].block_sight = False

def render_all():
    global fov_recompute, fov_map

    if fov_recompute:
        fov_recompute = False
        libtcod.map_compute_fov(fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
        for y in range(MAPHEIGHT):
            for x in range(MAPWIDTH):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = map[x][y].block_sight
                if not visible:
                    if map[x][y].explored:
                        if wall:
                            libtcod.console_set_char_background(con, x, y, color_dark_wall, libtcod.BKGND_SET)
                        else:
                            libtcod.console_set_char_background(con, x, y, color_dark_ground, libtcod.BKGND_SET)
                else:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, color_light_wall, libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, color_light_ground, libtcod.BKGND_SET)
                    map[x][y].explored = True

    for obj in objects:
        if obj != player:
            obj.draw()
    player.draw()

    libtcod.console_blit(con, 0, 0, MAPWIDTH, MAPHEIGHT, 0, 0, 0)
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    render_bar(1, 1, BAR_WIDTH, "HP", player.fighter.hp, player.fighter.max_hp, libtcod.light_red, libtcod.darker_red)
    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse())
    y = 1
    for (line, color) in game_msgs:
        libtcod.console_set_default_foreground(panel, color)
        libtcod.console_print_ex(panel, MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
        y += 1
    libtcod.console_blit(panel, 0, 0, SCREENWIDTH, PANELHEIGHT, 0, 0, PANEL_Y)

def make_map():
    global map

    map = [[Tile(True) for y in range(MAPHEIGHT)] for x in range(MAPWIDTH)]
    rooms = []
    num_rooms = 0

    for r in range(MAXROOMS):
        w = libtcod.random_get_int(0, ROOMMINSIZE, ROOMMAXSIZE)
        h = libtcod.random_get_int(0, ROOMMINSIZE, ROOMMAXSIZE)
        x = libtcod.random_get_int(0, 0, MAPWIDTH - w - 1)
        y = libtcod.random_get_int(0, 0, MAPHEIGHT - h - 1)

        new_room = Rect(x, y, w, h)

        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break

        if not failed:
            create_room(new_room)
            new_x, new_y = new_room.get_center()
            # prints room number(letter) in center of each room so you can see order of generation
            #room_no = Object(new_x, new_y, chr(65 + num_rooms), "room number", libtcod.white)
            #objects.insert(0, room_no)

            if num_rooms == 0:
                player.x, player.y = new_x, new_y

            else:
                prev_x, prev_y = rooms[num_rooms - 1].get_center()

                if libtcod.random_get_int(0, 0, 1) == 1:
                    create_h_tunnel(prev_x, new_x, prev_y)
                    create_v_tunnel(prev_y, new_y, new_x)
                else:
                    create_v_tunnel(prev_y, new_y, prev_x)
                    create_h_tunnel(prev_x, new_x, new_y)
            place_objects(new_room)
            rooms.append(new_room)
            num_rooms += 1

def create_h_tunnel(x1, x2, y):
    global map

    for x in range(min(x1, x2), max(x1, x2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False

def create_v_tunnel(y1, y2, x):
    global map

    for y in range(min(y1, y2), max(y1, y2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False

def player_move_or_attack(dx, dy):
    global fov_recompute

    x = player.x + dx
    y = player.y + dy

    target = None
    for obj in objects:
        if obj.fighter and obj.x == x and obj.y == y:
            target = obj
            break

    if target != None:
        player.fighter.attack(target)
    else:
        player.move(dx, dy)
        fov_recompute = True

def handle_keys():
    global fov_recompute, key

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    elif key.vk == libtcod.KEY_ESCAPE:
        return "exit"

    if game_state == "playing":
        if key.vk == libtcod.KEY_UP:
            player_move_or_attack(0, -1)
        elif key.vk == libtcod.KEY_DOWN:
            player_move_or_attack(0, 1)
        elif key.vk == libtcod.KEY_LEFT:
            player_move_or_attack(-1, 0)
        elif key.vk == libtcod.KEY_RIGHT:
            player_move_or_attack(1, 0)
        else:
            key_char = chr(key.c)
            if key_char == "g":
                for obj in objects:
                    if obj.x == player.x and obj.y == player.y and obj.item:
                        obj.item.pick_up()
                        break
            if key_char == "i":
                chosen_item = inventory_menu("Press the key next to an item to use it, or any other to cancel.\n")
                if chosen_item != None:
                    chosen_item.use()
            return "didnt-take-turn"

def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER, "{}: {}/{}".format(name, value, maximum))

def message(new_msg, color = libtcod.white):
    new_msg_lines = textwrap.wrap(new_msg, MSG_WIDTH)

    for line in new_msg_lines:
        if len(game_msgs) == MSG_HEIGHT:
            del game_msgs[0]

        game_msgs.append((line, color))

def get_names_under_mouse():
    global mouse

    x, y = mouse.cx, mouse.cy
    names = ", ".join([obj.name for obj in objects if obj.x == x and obj.y == y and libtcod.map_is_in_fov(fov_map, obj.x, obj.y)])
    return names.capitalize()

def menu(header, options, width):
    if len(options) > 26:
        raise ValueError("Cannot have a menu with more than 26 options.")
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, SCREENHEIGHT, header)
    height = len(options) + header_height

    window = libtcod.console_new(width, height)
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    y = header_height
    letter_index = ord("a")
    for option_text in options:
        text = "({}) {}".format(chr(letter_index), option_text)
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1

    x = SCREENWIDTH // 2 - width // 2
    y = SCREENHEIGHT // 2 - height // 2
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

    libtcod.console_flush()
    key = libtcod.console_wait_for_keypress(True)
    index = key.c - ord("a")
    if index >= 0 and index < len(options):
        return index
    return None

def inventory_menu(header):
    if len(inventory) == 0:
        options = ["Inventory is empty."]
    else:
        options = [item.name for item in inventory]
    index = menu(header, options, INVENTORY_WIDTH)
    if index == None or len(inventory) == 0:
        return None
    return inventory[index].item

def cast_heal():
    if player.fighter.hp == player.fighter.max_hp:
        message("You are already at full health.", libtcod.red)
        return "cancelled"

    message("Your wounds start to feel better!", libtcod.light_violet)
    player.fighter.heal(HEAL_AMOUNT)

def cast_lightning():
    monster = closest_monster(LIGHTNING_RANGE)
    if monster == None:
        message("No enemy is close enough to hit.", libtcod.red)
        return "cancelled"

    message("A lightning bolt strikes the {} with a loud thunder! The bolt does {} damage".format(monster.name, LIGHTNING_DAMAGE), libtcod.light_blue)
    monster.fighter.take_damage(LIGHTNING_DAMAGE)

libtcod.console_set_custom_font("arial10x10.png", libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREENWIDTH, SCREENHEIGHT, "Cool practice thing", False)
con = libtcod.console_new(MAPWIDTH, MAPHEIGHT)

panel = libtcod.console_new(SCREENWIDTH, PANELHEIGHT)

fighter_component = Fighter(30, 2, 5, death_function = player_death)

player = Object(0, 0, "@", "player", libtcod.white, True, fighter = fighter_component)
objects = [player]
game_msgs = []
inventory = []

make_map()

fov_map = libtcod.map_new(MAPWIDTH, MAPHEIGHT)
for y in range(MAPHEIGHT):
    for x in range(MAPWIDTH):
        libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)
fov_recompute = True

game_state = "playing"
player_action = None

message("Welcome stranger!", libtcod.red)

mouse = libtcod.Mouse()
key = libtcod.Key()

libtcod.sys_set_fps(LIMITFPS)

while not libtcod.console_is_window_closed():
    libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)
    render_all()
    libtcod.console_flush()

    for obj in objects:
        obj.clear()
    player_action = handle_keys()
    if player_action == "exit":
        break

    if game_state == "playing" and player_action != "didnt-take-turn":
        for obj in objects:
            if obj.ai:
                obj.ai.take_turn()
