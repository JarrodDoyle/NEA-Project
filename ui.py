import textwrap
from bearlibterminal import terminal
import libtcodpy as libtcod
from entities.entity_functions import get_visible_entities

class UI_Element:
    """
    Base UI Element class to be inherited by other UI elements
    """
    def __init__(self, x, y, w, h, title = None):
        """
        Initialize UI element

        x -- x coordinate of top left corner of ui element
        y -- y coordinate of top left corner of ui element
        w -- width of ui element
        h -- height of ui element
        title -- text to be written in center of the top border, defaults to NoneType
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.title = title

    def create_window(self, bk_color = "black", color = "white"):
        """
        Draw the UI element window

        bk_color -- the color of the window background, default is "black"
        color -- the color of the window foreground (e.g. the text), default is
        "white"
        """
        # Create buffer layer with given color to create a background for UI_Element without removing whats underneath
        base_color = terminal.state(terminal.TK_COLOR)
        base_layer = terminal.state(terminal.TK_LAYER)
        terminal.color(bk_color)
        terminal.layer(base_layer + 1)
        row = "█" * (self.w + 2)
        for y in range(self.y - 1, self.y + self.h + 1):
            terminal.puts(self.x - 1, y, row)
        terminal.layer(base_layer + 2)
        terminal.color(color)

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

        return base_color, base_layer

class Menu(UI_Element):
    """
    Menu UI element class, used for generic menu creation
    """
    def __init__(self, x, y, w, h, title, options, bk_color = "black", color = "white"):
        """
        Initialize menu element

        x -- x coordinate of top left corner of menu
        y -- y coordinate of top left corner of menu
        w -- width of menu
        h -- height of menu
        title -- text to be written in center of the top border, aka menu name
        """
        self.options = options
        self.bk_color = bk_color
        self.color = color
        super().__init__(x, y, w, h, title)

    def render(self):
        """
        Render menu
        """
        # Render the menu window
        base_color, base_layer = self.create_window(bk_color = self.bk_color, color = self.color)

        # Render menu options and associated choice keys
        letter_index = ord("a")
        for i in range(len(self.options)):
            terminal.puts(self.x, self.y + i, "{}) {}".format(chr(letter_index), self.options[i]))
            letter_index += 1

        # Reset terminal colours and layer
        terminal.color(base_color)
        terminal.layer(base_layer)

    def get_choice(self):
        """
        Return the menu option chosen or exit/quit
        """
        result = {}
        valid_choice = False
        while not valid_choice:
            choice = terminal.read()
            # If an option is chosen
            if choice - terminal.TK_A in range(len(self.options)):
                valid_choice = True
                result["choice"] = choice - terminal.TK_A
            # If menu cancelled
            elif choice == terminal.TK_ESCAPE:
                valid_choice = True
                result["cancel"] = True
            # If game quitted
            elif choice == terminal.TK_CLOSE:
                valid_choice = True
                result["quit"] = True
        return result

class Player_UI_Window(UI_Element):
    """
    UI Element for the players stats
    """
    def __init__(self):
        """
        Initialize player stat ui element
        """
        super().__init__(1, 1, 14, 13, "Player")

    def render(self, player):
        """
        Render the player stat window
        """
        # Create border for window and clear area
        base_color, base_layer = self.create_window()

        # LINE ONE
        # Display player name
        terminal.puts(self.x, self.y, "Name: {}".format(player.name))

        # LINE TWO
        # If player has bonus strength display strenght and then bonus strenght after
        if player.components["fighter"].bonus_stat("strength") > 0:
            terminal.puts(self.x, self.y + 1, "Str: [color=green]{}[/color] ([color=blue]+{}[/color])".format(player.components["fighter"].strength, player.components["fighter"].bonus_stat("strength")))
        # Otherwise just display strength
        else:
            terminal.puts(self.x, self.y + 1, "Str: [color=green]{}[/color]".format(player.components["fighter"].strength))

        # LINE THREE
        # If player has bonus defense display defense and then bonus defense after
        if player.components["fighter"].bonus_stat("defense") > 0:
            terminal.puts(self.x, self.y + 2, "Def: [color=green]{}[/color] ([color=blue]+{}[/color])".format(player.components["fighter"].defense, player.components["fighter"].bonus_stat("defense")))
        # Otherwise just display defense
        else:
            terminal.puts(self.x, self.y + 2, "Def: [color=green]{}[/color]".format(player.components["fighter"].defense))

        # LINE FOUR
        # If player has bonus accuracy display defense and then bonus accuracy after
        if player.components["fighter"].bonus_stat("accuracy") > 0:
            terminal.puts(self.x, self.y + 3, "Acc: [color=green]{}[/color] ([color=blue]+{}[/color])".format(player.components["fighter"].accuracy, player.components["fighter"].bonus_stat("accuracy")))
        # Otherwise just display accuracy
        else:
            terminal.puts(self.x, self.y + 3, "Acc: [color=green]{}[/color]".format(player.components["fighter"].accuracy))

        # LINE FIVE
        # If player has bonus intelligence display intelligence and then bonus intelligence after
        if player.components["fighter"].bonus_stat("intelligence") > 0:
            terminal.puts(self.x, self.y + 4, "Int: [color=green]{}[/color] ([color=blue]+{}[/color])".format(player.components["fighter"].intelligence, player.components["fighter"].bonus_stat("intelligence")))
        # Otherwise just display intelligence
        else:
            terminal.puts(self.x, self.y + 4, "Int: [color=green]{}[/color]".format(player.components["fighter"].intelligence))

        # LINE SIX
        # If player has bonus dexterity display dexterity and then bonus dexterity after
        if player.components["fighter"].bonus_stat("dexterity") > 0:
            terminal.puts(self.x, self.y + 5, "Dex: [color=green]{}[/color] ([color=blue]+{}[/color])".format(player.components["fighter"].dexterity, player.components["fighter"].bonus_stat("dexterity")))
        # Otherwise just display dexterity
        else:
            terminal.puts(self.x, self.y + 5, "Dex: [color=green]{}[/color]".format(player.components["fighter"].dexterity))

        # LINE EIGHT
        terminal.puts(self.x, self.y + 7, "Lvl: [color=orange]{}[/color]".format(player.components["level"].level))
        # LINE NINE
        terminal.puts(self.x, self.y + 8, "Exp: [color=orange]{}/{}[/color]".format(player.components["level"].xp, player.components["level"].level_up_xp))

        # LINE ELEVEN
        terminal.puts(self.x, self.y + 10, "Hp: [color=red]{}/{}[/color]".format(player.components["fighter"].hp, player.components["fighter"].max_hp))
        # LINE TWELVE
        health_bar(self.x, self.y + 11, self.w, 1, player)

        terminal.color(base_color)
        terminal.layer(base_layer)

class Inventory_UI_Window(UI_Element):
    """
    UI Element to display the players inventory
    """
    def __init__(self):
        """
        Initialize inventory ui element
        """
        super().__init__(65, 1, 30, 29, "Inventory")

    def render(self, player):
        """
        Render the players inventory screen menu
        """
        # Render window
        base_color, base_layer = self.create_window()
        inventory = player.components["inventory"].items
        letter_index = ord("a")
        dy = 0
        # List each item and how many of them the player has
        # Item_name -- name of item, items -- list of all occurances of the item
        for item_name, items in inventory.items():
            if item_name != "num_items":
                num_item = len(items)
                item = items[0]
                terminal.puts(self.x, self.y + dy, "{}) [color={}]{}[/color]".format(chr(letter_index), item.color, item_name))
                # If player has multiple of an item, say how many of them they have
                if num_item > 1:
                    dx = self.w - 3 - len(str(num_item))
                    terminal.puts(self.x + dx, self.y + dy, "(x{})".format(num_item))
                dy += 1
                letter_index += 1
        # Reset terminal colour and layer
        terminal.color(base_color)
        terminal.layer(base_layer)

class Generic_Text_Window(UI_Element):
    """
    UI Element used for generic text windows
    """
    def __init__(self, x, y, w, h, title):
        """
        Initialize text element

        x -- x coordinate of top left corner of text window
        y -- y coordinate of top left corner of text window
        w -- width of text window
        h -- height of text window
        title -- text to be written in center of the top border
        """
        super().__init__(x, y, w, h, title)

    def render(self, text):
        """
        Render UI element with text

        text -- the text to be drawn in the ui window
        """
        self.text = text
        base_color, base_layer = self.create_window()

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

        terminal.color(base_color)
        terminal.layer(base_layer)

class Dungeon_UI_Window(UI_Element):
    """
    UI Element to draw the dungeon floor in
    """
    def __init__(self):
        """
        Initialize dungeon window from parent class
        """
        super().__init__(17, 1, 46, 46, "Dungeon")

    # Render dungeon within UI Box
    def render(self, player, entities, dungeon, fov_map, fog_of_war):
        """
        Render dungeon floor within ui box

        player -- the player entity object
        entities -- list of entities on the dungeon floor
        dungeon -- dungeon floor object which holds a 2d array of cells
        fov_map -- field of view map based around the player
        fog_of_war -- boolean for whether to render fog of war or to render all
        cells
        """
        # Render window
        base_color, base_layer = self.create_window()

        # Get min/max x/y values of the dungeon to render so as to stay within the UI Box and decrease unneccesary terminal print calls
        x_min = max(17 - player.x_offset, 0)
        x_max = min(62 - player.x_offset, dungeon.width - 1)

        y_min = max(1 - player.y_offset, 0)
        y_max = min(46 - player.y_offset, dungeon.height - 1)
        # Render dungeon cells
        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                # If player can see the cell
                if visible:
                    # Set the cell to explored (so that it can be kept track of
                    # in the fog of war), and draw the cell
                    dungeon.tiles[y][x].explored = True
                    terminal.puts(x + player.x_offset, y + player.y_offset, "[color={}]{}[/color]".format(dungeon.tiles[y][x].color, dungeon.tiles[y][x].char))
                # draw the cell if it has been previously seen or fog of war is disabled
                elif (not visible and dungeon.tiles[y][x].explored) or not fog_of_war:
                    terminal.puts(x + player.x_offset, y + player.y_offset, "[color={}]{}[/color]".format(dungeon.tiles[y][x].bk_color, dungeon.tiles[y][x].char))

        # Order entity list according to their render order enum value
        entities_in_render_order = sorted(entities, key = lambda x: x.render_order.value)
        # Render entities
        for entity in entities_in_render_order:
            if entity.y in range(y_min, y_max + 1):
                if entity.x in range(x_min, x_max + 1):
                    # If fog of war is enable and the entity is in the players field
                    # of view, render them.
                    if fog_of_war:
                        visible = libtcod.map_is_in_fov(fov_map, entity.x, entity.y)
                        if visible:
                            terminal.puts(entity.x + player.x_offset, entity.y + player.y_offset, "[color={}]{}[/color]".format(entity.color, entity.char))
                    # If fog of war is not enabled simply render all entities
                    else:
                        terminal.puts(entity.x + player.x_offset, entity.y + player.y_offset, "[color={}]{}[/color]".format(entity.color, entity.char))

        # Reset terminal colour and layer
        terminal.color(base_color)
        terminal.layer(base_layer)

class Monsters_UI_Window(UI_Element):
    """
    UI element for rendering visible monsters
    """
    def __init__(self):
        """
        Initialize visible monsters UI
        """
        super().__init__(1, 16, 14, 31, "Monsters")

    def render(self, player, entities, fov_map):
        """
        Render ui element

        player -- the player entity object
        entities -- list of entities on the dungeon floor
        fov_map -- map of the players field of view
        """
        # Render the ui element window
        base_color, base_layer = self.create_window()
        # get a list of visible entities
        visible_entities = get_visible_entities(player, entities, fov_map)
        # If there are visible entities
        if visible_entities:
            num_monsters = 0
            # List a maximum of 7 monsters
            for i in range(min(len(visible_entities), 8)):
                if visible_entities[i].components.get("fighter"):
                    entity = visible_entities[i]
                    terminal.puts(self.x, self.y + num_monsters * 4, "[color={}]{}[/color]".format(entity.color, entity.name.capitalize()))
                    terminal.puts(self.x, self.y + num_monsters * 4 + 1, "Hp: [color=red]{}/{}[/color]".format(entity.components["fighter"].hp, entity.components["fighter"].max_hp))
                    health_bar(self.x, self.y + num_monsters * 4 + 2, 14, 1, entity)
                    num_monsters += 1
        # Reset terminal colour and layer
        terminal.color(base_color)
        terminal.layer(base_layer)

class Messages_UI_Window(UI_Element):
    """
    UI element for game messages
    """
    def __init__(self):
        """
        Initialize messages ui element from parent class
        """
        super().__init__(1, 49, 62, 14, "Message Log")
        self.messages = [] # list of messages the player recieved

    def render(self):
        """
        Render the messages UI
        """
        # Render window
        base_color, base_layer = self.create_window()
        # For each message
        for i in range(0, len(self.messages)):
            index = len(self.messages) - 1 - i
            # If message would be out of the ui window borders stop drawing messages
            if self.y + self.h - 1 - i < self.y:
                break
            message = self.messages[index]
            terminal.puts(self.x, self.y + self.h - 1 - i, message)
        # Reset terminal color and layer
        terminal.color(base_color)
        terminal.layer(base_layer)

class Description_UI_Window(UI_Element):
    """
    Description UI element inheriting from UI_Element
    """
    def __init__(self):
        """
        Initialize description UI element from parent class
        """
        super().__init__(65, 32, 30, 15, "Description")
        self.text = ""

    def render(self):
        """
        Render description UI Element
        """
        # Render description window
        base_color, base_layer = self.create_window()

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
        # Reset terminal colour and layer
        terminal.color(base_color)
        terminal.layer(base_layer)

class Equipment_UI_Window(UI_Element):
    """
    Equipment UI element inheriting from UI_Element
    """
    def __init__(self):
        """
        Initialize equipment ui element from parent class
        """
        super().__init__(65, 49, 30, 14, "Equipment")

    def render(self, equipment):
        """
        Render Equipment UI element

        equipment -- dictionary of equipment pieces
        """
        # Render equipment window
        base_color, base_layer = self.create_window("black")
        letter_index = ord("a")
        # Equipment line offset
        dy = 0
        # For each slot in equipment dict
        for i in equipment:
            equipment_piece = equipment.get(i)
            # If equipment piece in the slot
            if equipment_piece is not None:
                # Write the equipment piece/ammo count
                try:
                    terminal.puts(self.x, self.y + dy, "{}) {}: [color={}]{}[/color]".format(chr(letter_index + dy), i.capitalize(), equipment.get(i).color, equipment.get(i).name))
                except:
                    terminal.puts(self.x, self.y + dy, "{}) {}: {}".format(chr(letter_index + dy), i.capitalize(), equipment.get(i)))
            # Otherwise just write the slot name
            else:
                terminal.puts(self.x, self.y + dy, "{}) {}:".format(chr(letter_index + dy), i.capitalize()))
            dy += 1
        # Reset terminal colour and layer
        terminal.color(base_color)
        terminal.layer(base_layer)

def health_bar(x, y, w, h, entity):
    """
    Render health bar for an entity
    """
    # Calculate percentage of health
    percent_health = entity.components["fighter"].hp / entity.components["fighter"].max_hp
    # Calculate how much of the health bar should be filled
    filled_x = x + int(w * percent_health) - 1
    # Render health bar
    for y in range(y, y + h):
        for x in range(x, x + w):
            if x <= filled_x:
                terminal.puts(x, y, "[color=red]█[/color]")
            else:
                terminal.puts(x, y, "[color=darker red]█[/color]")

def initialize_ui_elements():
    """
    Return dict of all UI Elements
    """
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
