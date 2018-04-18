import libtcodpy as libtcod

def get_visible_entities(player, entities, fov_map):
    """
    Calculate and return a list of entities in the player field of view
    """
    visible_entities = []
    # For every non-player entity
    for entity in entities:
        if entity != player:
            # If entity in player FOV add it to the list
            visible = libtcod.map_is_in_fov(fov_map, entity.x, entity.y)
            if visible:
                visible_entities.append(entity)
    # If there are visible entities return them, otherwise return None
    if len(visible_entities) > 0:
        return visible_entities
    else:
        return None

def get_blocking_entity(entities, x, y):
    """
    Return blocking entity at target location or None if no blocking entity exists
    """
    # For each entity
    for entity in entities:
        # If entity at target location and entity blocks
        if entity.x == x and entity.y == y and entity.blocks:
            return entity
    # Otherwise return nothing
    else:
        return None
