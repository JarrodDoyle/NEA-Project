from bearlibterminal import terminal
import libtcodpy as libtcod
from entities import *

def create_window(x, y, w, h, title = None):
    # Clear window area
    terminal.clear_area(x - 1, y - 1, w + 2, h + 2)

    # create top border
    border_top = "╔" + "═" * (w) + "╗"
    terminal.puts(x - 1, y - 1, border_top)

    # create side borders
    for i in range(h):
        terminal.puts(x - 1, y + i, "║")
        terminal.puts(x + w, y + i, "║")

    # create bottom border
    border_bottom = "╚" + "═" * (w) + "╝"
    terminal.puts(x - 1, y + h, border_bottom)

    if title:
        offset = (w + 2 - len(title)) // 2 - 1
        terminal.puts(x + offset, y - 1, title)

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

def inventory_window(player):
    x = 65
    y = 1
    w = 30
    h = 29
    title = "Inventory"
    create_window(x, y, w, h, title)

    inventory = player.inventory

    letter_index = ord("a")
    for i in range(len(inventory)):
        terminal.puts(x, y + i, "{}) {}".format(chr(letter_index + i), inventory[i]))

def player_window(player):
    x, y, w, h, title = 1, 1, 14, 12, "Player"
    create_window(x, y, w, h, title)

    terminal.puts(x, y, "Name: {}".format(player.name))
    if player.fighter.bonus_strength() > 0:
        terminal.puts(x, y + 1, "Str: [color=green]{}[/color] ([color=blue]+{}[/color])".format(player.fighter.strength, player.fighter.bonus_strength()))
    else:
        terminal.puts(x, y + 1, "Str: [color=green]{}[/color]".format(player.fighter.strength))

    if player.fighter.bonus_defense() > 0:
        terminal.puts(x, y + 2, "Def: [color=green]{}[/color] ([color=blue]+{}[/color])".format(player.fighter.defense, player.fighter.bonus_defense()))
    else:
        terminal.puts(x, y + 2, "Def: [color=green]{}[/color]".format(player.fighter.defense))

    if player.fighter.bonus_intelligence() > 0:
        terminal.puts(x, y + 3, "Int: [color=green]{}[/color] ([color=blue]+{}[/color])".format(player.fighter.intelligence, player.fighter.bonus_intelligence()))
    else:
        terminal.puts(x, y + 3, "Int: [color=green]{}[/color]".format(player.fighter.intelligence))

    # TODO: implement level stuff
    terminal.puts(x, y + 5, "Lvl: [color=orange]{}[/color]".format(1))
    terminal.puts(x, y + 6, "Exp: [color=orange]{}[/color]".format(0))

    terminal.puts(x, y + 8, "Hp: [color=red]{}/{}[/color]".format(player.fighter.hp, player.fighter.max_hp))
    health_bar(x, y + 9, 14, 1, player)

    terminal.puts(x, y + 11, "Gold: [color=yellow]{}[/color]".format(200)) # Replace with players gold amount

def dungeon_window(player, dungeon, fov_map):
    x, y, w, h, title = 17, 1, 46, 46, "Dungeon"
    create_window(x, y, w, h, title)

    for y in range(len(dungeon)):
        for x in range(len(dungeon[0])):
            if 17 <= x + player.x_offset <= 62 and 1 <= y + player.y_offset <= 46:
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                if not visible and dungeon[y][x].explored:
                    terminal.puts(x + player.x_offset, y + player.y_offset, "[color={}]{}[/color]".format(dungeon[y][x].base_bk_color, dungeon[y][x].base_char))
                elif visible:
                    dungeon[y][x].explored = True
                    terminal.puts(x + player.x_offset, y + player.y_offset, "[color={}]{}[/color]".format(dungeon[y][x].color, dungeon[y][x].char))

def monsters_window(player, entities, fov_map):
    x, y, w, h, title = 1, 15, 14, 32, "Monsters"
    create_window(x, y, w, h, title)

    visible_entities = get_visible_entities(player, entities, fov_map)
    for i in range(len(visible_entities)):
        if visible_entities[i].fighter:
            entity = visible_entities[i]
            terminal.puts(x, y + i * 5, "[color={}]{}[/color]".format(entity.color, entity.name.capitalize()))
            terminal.puts(x, y + i * 5 + 1, "Hp: [color=red]{}/{}[/color]".format(entity.fighter.hp, entity.fighter.max_hp))
            health_bar(x, y + i * 5 + 2, 14, 1, entity)

def messages_window(messages):
    x, y, w, h, title = 1, 49, 62, 14, "Message Log"
    create_window(x, y, w, h, title)

    for i in range(0, len(messages)):
        index = len(messages) - 1 - i
        if y + h - 1 - i < y:
            break
        message = messages[index]
        terminal.puts(x, y + h - 1 - i, message)

def description_window():
    x, y, w, h, title = 65, 32, 30, 15, "Description"
    create_window(x, y, w, h, title)

def equipment_window():
    x, y, w, h, title = 65, 49, 30, 14, "Equipment"
    create_window(x, y, w, h, title)

if __name__ == "__main__":
    ui_elements =  [player_menu, dungeon_menu, inventory_menu, monsters_menu, messages_menu, description_menu, equipment_menu]
    terminal.open()
    terminal.set("window: size=96x64; font: 'font_12x12.png', size=12x12, codepage=437")
    while True:
        for e in ui_elements:
            e()
        terminal.refresh()
        if terminal.read() == terminal.TK_CLOSE:
            terminal.close()
            break
