import textwrap
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

    def create_window(self, color):
        # Create buffer layer with given color to create a background for UI_Element without removing whats underneath
        base_layer = terminal.state(terminal.TK_LAYER)
        base_color = terminal.state(terminal.TK_COLOR)
        terminal.layer(base_layer + 1)
        terminal.color(color)
        row = "█" * (self.w + 2)
        for y in range(self.y - 1, self.y + self.h + 1):
            terminal.puts(self.x - 1, y, row)
        terminal.layer(base_layer + 2)
        terminal.color("white") # TODO: make it return to previous color properly

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

        # Draw title if one is given
        if self.title:
            offset = (self.w + 2 - len(self.title)) // 2 - 1
            terminal.puts(self.x + offset, self.y - 1, self.title)

        return base_layer

class Menu(UI_Element):
    def __init__(self, x, y, w, h, title, options, bk_color):
        self.options = options
        self.bk_color = bk_color
        super().__init__(x, y, w, h, title)

    def render(self):
        base_layer = self.create_window(self.bk_color)

        letter_index = ord("a")
        for i in range(len(self.options)):
            terminal.puts(self.x, self.y + i, "{}) {}".format(chr(letter_index), self.options[i]))
            letter_index += 1

        terminal.layer(base_layer)

    def get_choice(self):
        valid_choice = False
        while not valid_choice:
            choice = terminal.read()
            if choice - terminal.TK_A in range(len(self.options)):
                valid_choice = True
        return choice - terminal.TK_A

class Player_UI_Window(UI_Element):
    def __init__(self):
        super().__init__(1, 1, 14, 13, "Player")
        # height = window height - 31

    def render(self, player):
        # Create border for window and clear area
        base_layer = self.create_window("black")

        # LINE ONE
        # Display player name
        terminal.puts(self.x, self.y, "Name: {}".format(player.name))

        # LINE TWO
        # If player has bonus strength display strenght and then bonus strenght after
        if player.components["fighter"].bonus_strength() > 0:
            terminal.puts(self.x, self.y + 1, "Str: [color=green]{}[/color] ([color=blue]+{}[/color])".format(player.components["fighter"].strength, player.components["fighter"].bonus_strength()))
        # Otherwise just display strength
        else:
            terminal.puts(self.x, self.y + 1, "Str: [color=green]{}[/color]".format(player.components["fighter"].strength))

        # LINE THREE
        # If player has bonus defense display defense and then bonus defense after
        if player.components["fighter"].bonus_defense() > 0:
            terminal.puts(self.x, self.y + 2, "Def: [color=green]{}[/color] ([color=blue]+{}[/color])".format(player.components["fighter"].defense, player.components["fighter"].bonus_defense()))
        # Otherwise just display defense
        else:
            terminal.puts(self.x, self.y + 2, "Def: [color=green]{}[/color]".format(player.components["fighter"].defense))

        # LINE FOUR
        # If player has bonus accuracy display defense and then bonus accuracy after
        if player.components["fighter"].bonus_accuracy() > 0:
            terminal.puts(self.x, self.y + 3, "Acc: [color=green]{}[/color] ([color=blue]+{}[/color])".format(player.components["fighter"].accuracy, player.components["fighter"].bonus_accuracy()))
        # Otherwise just display accuracy
        else:
            terminal.puts(self.x, self.y + 3, "Acc: [color=green]{}[/color]".format(player.components["fighter"].accuracy))

        # LINE FIVE
        # If player has bonus intelligence display intelligence and then bonus intelligence after
        if player.components["fighter"].bonus_intelligence() > 0:
            terminal.puts(self.x, self.y + 4, "Int: [color=green]{}[/color] ([color=blue]+{}[/color])".format(player.components["fighter"].intelligence, player.components["fighter"].bonus_intelligence()))
        # Otherwise just display intelligence
        else:
            terminal.puts(self.x, self.y + 4, "Int: [color=green]{}[/color]".format(player.components["fighter"].intelligence))

        # LINE SEVEN
        terminal.puts(self.x, self.y + 6, "Lvl: [color=orange]{}[/color]".format(player.components["level"].level))
        # LINE EIGHT
        terminal.puts(self.x, self.y + 7, "Exp: [color=orange]{}/{}[/color]".format(player.components["level"].xp, player.components["level"].level_up_xp))

        # LINE TEN
        terminal.puts(self.x, self.y + 9, "Hp: [color=red]{}/{}[/color]".format(player.components["fighter"].hp, player.components["fighter"].max_hp))
        # LINE ELEVEN
        health_bar(self.x, self.y + 10, self.w, 1, player)

        # LINE THIRTEEN
        terminal.puts(self.x, self.y + 12, "Gold: [color=yellow]{}[/color]".format(200)) # TODO: Replace with players gold amount

        terminal.layer(base_layer)

class Inventory_UI_Window(UI_Element):
    def __init__(self):
        super().__init__(65, 1, 30, 29, "Inventory")

    def render(self, player):
        base_layer = self.create_window("black")
        inventory = player.components["inventory"].items
        letter_index = ord("a")
        num_item = 0
        dy = 0
        if len(inventory) > 0:
            current_item = inventory[0]
        for i in range(len(inventory)):
            if inventory[i].name == current_item.name:
                num_item += 1
                terminal.puts(self.x, self.y + dy, "{}) [color={}]{}[/color]".format(chr(letter_index), inventory[i].color, inventory[i].name))
                if num_item > 1:
                    dx = self.w - 3 - len(str(num_item))
                    terminal.puts(self.x + dx, self.y + dy, "(x{})".format(num_item))
            else:
                dy += 1
                letter_index += 1
                terminal.puts(self.x, self.y + dy, "{}) [color={}]{}[/color]".format(chr(letter_index), inventory[i].color, inventory[i].name))

        terminal.layer(base_layer)

class Dungeon_UI_Window(UI_Element):
    # Initialize from parent UI_Element class
    def __init__(self):
        super().__init__(17, 1, 46, 46, "Dungeon")

    # Render dungeon within UI Box
    def render(self, player, entities, dungeon, fov_map, fog_of_war):
        base_layer = self.create_window("black")

        # Get min/max x/y values of the dungeon to render so as to stay within the UI Box and decrease unneccesary terminal print calls
        x_min = max(17 - player.x_offset, 0)
        x_max = min(62 - player.x_offset, dungeon.width - 1)

        y_min = max(1 - player.y_offset, 0)
        y_max = min(46 - player.y_offset, dungeon.height - 1)
        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                if visible:
                    dungeon.tiles[y][x].explored = True
                    terminal.puts(x + player.x_offset, y + player.y_offset, "[color={}]{}[/color]".format(dungeon.tiles[y][x].color, dungeon.tiles[y][x].char))
                elif (not visible and dungeon.tiles[y][x].explored) or not fog_of_war:
                    terminal.puts(x + player.x_offset, y + player.y_offset, "[color={}]{}[/color]".format(dungeon.tiles[y][x].bk_color, dungeon.tiles[y][x].char))

        entities_in_render_order = sorted(entities, key = lambda x: x.render_order.value)
        for entity in entities_in_render_order:
            if entity.y in range(y_min, y_max + 1):
                if entity.x in range(x_min, x_max + 1):
                    if fog_of_war:
                        visible = libtcod.map_is_in_fov(fov_map, entity.x, entity.y)
                        if visible:
                            terminal.puts(entity.x + player.x_offset, entity.y + player.y_offset, "[color={}]{}[/color]".format(entity.color, entity.char))
                    else:
                        terminal.puts(entity.x + player.x_offset, entity.y + player.y_offset, "[color={}]{}[/color]".format(entity.color, entity.char))

        terminal.layer(base_layer)

class Monsters_UI_Window(UI_Element):
    def __init__(self):
        super().__init__(1, 16, 14, 31, "Monsters")

    def render(self, player, entities, fov_map):
        base_layer = self.create_window("black")

        visible_entities = get_visible_entities(player, entities, fov_map)
        if visible_entities:
            num_monsters = 0
            for i in range(min(len(visible_entities), 8)):
                if visible_entities[i].components.get("fighter"):
                    entity = visible_entities[i]
                    terminal.puts(self.x, self.y + num_monsters * 4, "[color={}]{}[/color]".format(entity.color, entity.name.capitalize()))
                    terminal.puts(self.x, self.y + num_monsters * 4 + 1, "Hp: [color=red]{}/{}[/color]".format(entity.components["fighter"].hp, entity.components["fighter"].max_hp))
                    health_bar(self.x, self.y + num_monsters * 4 + 2, 14, 1, entity)
                    num_monsters += 1

        terminal.layer(base_layer)

class Messages_UI_Window(UI_Element):
    def __init__(self):
        super().__init__(1, 49, 62, 14, "Message Log")
        self.messages = []

    def render(self):
        base_layer = self.create_window("black")
        for i in range(0, len(self.messages)):
            index = len(self.messages) - 1 - i
            if self.y + self.h - 1 - i < self.y:
                break
            message = self.messages[index]
            terminal.puts(self.x, self.y + self.h - 1 - i, message)

        terminal.layer(base_layer)

class Description_UI_Window(UI_Element):
    def __init__(self):
        super().__init__(65, 32, 30, 15, "Description")
        self.text = ""

    def render(self):
        base_layer = self.create_window("black")

        # Turn text into a list of non-textwrapped lines
        text = []
        line = ""
        for i in self.text:
            if i != "\n":
                line += i
            else:
                text.append(line)
                line = ""
        if len(line) > 0:
            text.append(line)

        # Get a final list of the lines in description by word wrapping the previously created text list
        description = []
        for i in text:
            description += textwrap.wrap(i, width = self.w)

        if len(description) > self.h:
            raise Exception("Description is too long")

        for i in range(len(description)):
            terminal.puts(self.x, self.y + i, description[i])
        # Reset description text
        self.text = ""

        terminal.layer(base_layer)

class Equipment_UI_Window(UI_Element):
    def __init__(self):
        super().__init__(65, 49, 30, 14, "Equipment")

    def render(self, equipment):
        base_layer = self.create_window("black")
        letter_index = ord("a")
        dy = 0
        for i in equipment:
            equipment_piece = equipment.get(i)
            if equipment_piece is not None:
                terminal.puts(self.x, self.y + dy, "{}) {}: [color={}]{}[/color]".format(chr(letter_index + dy), i, equipment.get(i).color, equipment.get(i).name))
            else:
                terminal.puts(self.x, self.y + dy, "{}) {}:".format(chr(letter_index + dy), i))
            dy += 1

        terminal.layer(base_layer)

def health_bar(x, y, w, h, entity):
    percent_health = entity.components["fighter"].hp / entity.components["fighter"].max_hp
    filled_x = x + int(w * percent_health) - 1
    for y in range(y, y + h):
        for x in range(x, x + w):
            if x <= filled_x:
                terminal.puts(x, y, "[color=red]█[/color]")
            else:
                terminal.puts(x, y, "[color=darker red]█[/color]")

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
