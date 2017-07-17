from bearlibterminal import terminal
import libtcodpy as libtcod
from fov_functions import *
from ui import *

def render(dungeon, player, entities, fov_map, fov_recompute):
    terminal.clear()
    recompute_fov(fov_recompute, fov_map, player)
    player_window(player)
    monsters_window(player, entities, fov_map)
    messages_window(player.messages)
    equipment_window()
    description_window()
    inventory_window(player)
    dungeon_window(player, dungeon, fov_map)
    terminal.refresh()
