from bearlibterminal import terminal
import libtcodpy as libtcod
from fov_functions import *
from ui import *

def render(dungeon, player, entities, fov_map, fov_recompute, ui_elements):
    #terminal.clear()
    recompute_fov(fov_recompute, fov_map, player)
    if ui_elements["player"].redraw:
        ui_elements["player"].render(player)
        ui_elements["player"].redraw = False

    if ui_elements["monsters"].redraw:
        ui_elements["monsters"].render(player, entities, fov_map)
        ui_elements["monsters"].redraw = False

    if ui_elements["messages"].redraw:
        ui_elements["messages"].render(player.messages)
        ui_elements["messages"].redraw = False

    if ui_elements["equipment"].redraw:
        ui_elements["equipment"].render()
        ui_elements["equipment"].redraw = False

    if ui_elements["description"].redraw:
        ui_elements["description"].render()
        ui_elements["description"].redraw = False

    if ui_elements["inventory"].redraw:
        ui_elements["inventory"].render(player)
        ui_elements["inventory"].redraw = False

    if ui_elements["dungeon"].redraw:
        ui_elements["dungeon"].render(player, dungeon, fov_map)
        ui_elements["dungeon"].redraw = False
    terminal.refresh()
