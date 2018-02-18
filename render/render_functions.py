from bearlibterminal import terminal
import libtcodpy as libtcod
from fov_functions import *
from ui import *

def render(dungeon = None, player = None, entities = None, fov_map = None, fov_recompute = None, ui_elements = None, fog_of_war = None):
    terminal.clear()
    recompute_fov(fov_recompute, fov_map, player)
    if player != None:
        ui_elements["player"].render(player)
        ui_elements["equipment"].render(player.components.get("equipment").equipment)
        ui_elements["inventory"].render(player)
        if entities != None and fov_map != None:
            ui_elements["monsters"].render(player, entities, fov_map)
            if dungeon != None and fog_of_war != None:
                ui_elements["dungeon"].render(player, entities, dungeon, fov_map, fog_of_war)
    ui_elements["messages"].render()
    ui_elements["description"].render()
    terminal.refresh()
