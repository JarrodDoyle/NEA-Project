import libtcodpy as libtcod
from bearlibterminal import terminal

def recompute_fov(fov_recompute, fov_map, player):
    """
    Recompute the field of view

    fov_recompute -- Boolean for whether to recompute field of view
    fov_map -- current fov map to be updated
    player -- the entity whose field of view is calculated
    """
    if fov_recompute:
        fov_recompute = False
        libtcod.map_compute_fov(fov_map, player.x, player.y, 10, True, 0)

def initialize_fov(dungeon):
    """
    Return base field of view map of the passed dungeon
    """
    w = dungeon.width
    h = dungeon.height
    fov_map = libtcod.map_new(w, h) # Create a new LibTCOD map
    fov_recompute = True
    for y in range(h):
        for x in range(w):
            # Updates map cells based on walkability and visibility
            libtcod.map_set_properties(fov_map, x, y, not dungeon.tiles[y][x].blocks_sight, not dungeon.tiles[y][x].is_blocked)
    return fov_map, fov_recompute
