import libtcodpy as libtcod
from bearlibterminal import terminal

def recompute_fov(fov_recompute, fov_map, player):
    if fov_recompute:
        fov_recompute = False
        libtcod.map_compute_fov(fov_map, player.x, player.y, 10, True, 0)

def initialize_fov(dungeon):
    w = dungeon.width
    h = dungeon.height
    fov_map = libtcod.map_new(w, h)
    fov_recompute = True
    for y in range(h):
        for x in range(w):
            libtcod.map_set_properties(fov_map, x, y, not dungeon.tiles[y][x].blocks_sight, not dungeon.tiles[y][x].is_blocked)
    return fov_map, fov_recompute
