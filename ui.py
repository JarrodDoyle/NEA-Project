from bearlibterminal import terminal
import libtcodpy as libtcod
from entities.entity_functions import get_visible_entities

class UI_Element:
    def __init__(self, x, y, w, h, title = None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.title = title

    def create_window(self):
        # Clear window area
        terminal.clear_area(self.x - 1, self.y - 1, self.w + 2, self.h + 2)

        # create top border
        border_top = "╔" + "═" * (self.w) + "╗"
        terminal.puts(self.x - 1, self.y - 1, border_top)

        # create side borders
        for i in range(self.h):
            terminal.puts(self.x - 1, self.y + i, "║")
            terminal.puts(self.x + self.w, self.y + i, "║")

        # create bottom border
        border_bottom = "╚" + "═" * (self.w) + "╝"
        terminal.puts(self.x - 1, self.y + self.h, border_bottom)

        if self.title:
            offset = (self.w + 2 - len(self.title)) // 2 - 1
            terminal.puts(self.x + offset, self.y - 1, self.title)

class Player_UI_Window(UI_Element):
    def __init__(self):
        super().__init__(1, 1, 14, 13, "Player")

    def render(self, player):
        # Create border for window and clear area
        self.create_window()

        # LINE ONE
        # Display player name
        terminal.puts(self.x, self.y, f"Name: {player.name}")

        # LINE TWO
        # If player has bonus strength display strenght and then bonus strenght after
        if player.fighter.bonus_strength() > 0:
            terminal.puts(self.x, self.y + 1, f"Str: [color=green]{player.fighter.strength}[/color] ([color=blue]+{player.fighter.bonus_strength()}[/color])")
        # Otherwise just display strength
        else:
            terminal.puts(self.x, self.y + 1, f"Str: [color=green]{player.fighter.strength}[/color]")

        # LINE THREE
        # If player has bonus defense display defense and then bonus defense after
        if player.fighter.bonus_defense() > 0:
            terminal.puts(self.x, self.y + 2, f"Def: [color=green]{player.fighter.defense}[/color] ([color=blue]+{player.fighter.bonus_defense()}[/color])")
        # Otherwise just display defense
        else:
            terminal.puts(self.x, self.y + 2, f"Def: [color=green]{player.fighter.defense}[/color]")

        # LINE FOUR
        # If player has bonus accuracy display defense and then bonus accuracy after
        if player.fighter.bonus_accuracy() > 0:
            terminal.puts(self.x, self.y + 3, f"Acc: [color=green]{player.fighter.accuracy}[/color] ([color=blue]+{player.fighter.bonus_accuracy()}[/color])")
        # Otherwise just display accuracy
        else:
            terminal.puts(self.x, self.y + 3, f"Acc: [color=green]{player.fighter.accuracy}[/color]")

        # LINE FIVE
        # If player has bonus intelligence display intelligence and then bonus intelligence after
        if player.fighter.bonus_intelligence() > 0:
            terminal.puts(self.x, self.y + 4, f"Int: [color=green]{player.fighter.intelligence}[/color] ([color=blue]+{player.fighter.bonus_intelligence()}[/color])")
        # Otherwise just display intelligence
        else:
            terminal.puts(self.x, self.y + 4, f"Int: [color=green]{player.fighter.intelligence}[/color]")

        # TODO: implement level stuff
        # LINE SEVEN
        terminal.puts(self.x, self.y + 6, f"Lvl: [color=orange]{1}[/color]")
        # LINE EIGHT
        terminal.puts(self.x, self.y + 7, f"Exp: [color=orange]{0}[/color]")

        # LINE TEN
        terminal.puts(self.x, self.y + 9, f"Hp: [color=red]{player.fighter.hp}/{player.fighter.max_hp}[/color]")
        # LINE ELEVEN
        health_bar(self.x, self.y + 10, self.w, 1, player)

        # LINE THIRTEEN
        terminal.puts(self.x, self.y + 12, f"Gold: [color=yellow]{200}[/color]") # Replace with players gold amount

class Inventory_UI_Window(UI_Element):
    def __init__(self):
        super().__init__(65, 1, 30, 29, "Inventory")

    def render(self, player):
        self.create_window()
        inventory = player.inventory.items
        letter_index = ord("a")
        for i in range(len(inventory)):
            terminal.puts(self.x, self.y + i, f"{chr(letter_index + i)}) [color={inventory[i].color}]{inventory[i].name}[/color]")

class Dungeon_UI_Window(UI_Element):
    def __init__(self):
        super().__init__(17, 1, 46, 46, "Dungeon")

    def render(self, player, entities, dungeon, fov_map):
        self.create_window()

        x_min = max(17 - player.x_offset, 0)
        x_max = min(62 - player.x_offset, dungeon.width - 1)

        y_min = max(1 - player.y_offset, 0)
        y_max = min(46 - player.y_offset, dungeon.height - 1)
        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                if not visible and dungeon.tiles[y][x].explored:
                    terminal.puts(x + player.x_offset, y + player.y_offset, f"[color={dungeon.tiles[y][x].bk_color}]{dungeon.tiles[y][x].char}[/color]")
                elif visible:
                    dungeon.tiles[y][x].explored = True
                    terminal.puts(x + player.x_offset, y + player.y_offset, f"[color={dungeon.tiles[y][x].color}]{dungeon.tiles[y][x].char}[/color]")

        entities_in_render_order = sorted(entities, key = lambda x: x.render_order.value)
        for entity in entities_in_render_order:
            visible = libtcod.map_is_in_fov(fov_map, entity.x, entity.y)
            if visible:
                terminal.puts(entity.x + player.x_offset, entity.y + player.y_offset, f"[color={entity.color}]{entity.char}[/color]")

class Monsters_UI_Window(UI_Element):
    def __init__(self):
        super().__init__(1, 16, 14, 32, "Monsters")

    def render(self, player, entities, fov_map):
        self.create_window()

        visible_entities = get_visible_entities(player, entities, fov_map)
        if visible_entities:
            num_monsters = 0
            for i in range(min(len(visible_entities), 8)):
                if visible_entities[i].fighter:
                    entity = visible_entities[i]
                    terminal.puts(self.x, self.y + num_monsters * 4, f"[color={entity.color}]{entity.name.capitalize()}[/color]")
                    terminal.puts(self.x, self.y + num_monsters * 4 + 1, f"Hp: [color=red]{entity.fighter.hp}/{entity.fighter.max_hp}[/color]")
                    health_bar(self.x, self.y + num_monsters * 4 + 2, 14, 1, entity)
                    num_monsters += 1

class Messages_UI_Window(UI_Element):
    def __init__(self):
        super().__init__(1, 49, 62, 14, "Message Log")
        self.messages = []

    def render(self):
        self.create_window()

        for i in range(0, len(self.messages)):
            index = len(self.messages) - 1 - i
            if self.y + self.h - 1 - i < self.y:
                break
            message = self.messages[index]
            terminal.puts(self.x, self.y + self.h - 1 - i, message)

class Description_UI_Window(UI_Element):
    def __init__(self):
        super().__init__(65, 32, 30, 15, "Description")

    def render(self):
        self.create_window()

class Equipment_UI_Window(UI_Element):
    def __init__(self):
        super().__init__(65, 49, 30, 14, "Equipment")

    def render(self):
        self.create_window()

def health_bar(x, y, w, h, entity):
    percent_health = entity.fighter.hp / entity.fighter.max_hp
    filled_x = x + int(w * percent_health) - 1
    for y in range(y, y + h):
        for x in range(x, x + w):
            if x <= filled_x:
                terminal.puts(x, y, "[bkcolor=red] [/color]")
            else:
                terminal.puts(x, y, "[bkcolor=darker red] [/color]")

def menu():
    pass

def initialize_ui_elements():
    ui_elements = {
                    "player": Player_UI_Window(),
                    "monsters": Monsters_UI_Window(),
                    "messages": Messages_UI_Window(),
                    "equipment": Equipment_UI_Window(),
                    "description": Description_UI_Window(),
                    "inventory": Inventory_UI_Window(),
                    "dungeon": Dungeon_UI_Window()
    }

    return ui_elements
