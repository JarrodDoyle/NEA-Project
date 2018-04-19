from ui import Menu
from bearlibterminal import terminal

def get_targets(entity, entity_list, target_range, entity_type = None):
    """
    Return a list of valid target entities

    entity -- the entity doing the targetting
    entity_list -- list of entities on the dungeon floor that could potentially
    be targetted
    target_range -- the range from the entity that target entities can be
    entity_type -- the type of entity to target, default is None meaning all
    entity types can be considered for targetting
    """
    targets = []
    for other_entity in entity_list:
        # If no entity type preference
        if entity_type is None:
            # If within range of the targetting entity add it to the targets list
            if other_entity != entity and entity.distance_to(other_entity) < target_range + 1:
                targets.append(other_entity)
        else:
            # If of correct entity type and within range of the targetting entity,
            # add it to the targets list
            if other_entity != entity and other_entity.components.get(entity_type) and entity.distance_to(other_entity) < target_range + 1:
                targets.append(other_entity)
    return targets

def choose_target(entity, entity_list, target_range, entity_type = None):
    """
    Choose an entity within a specified range to target
    """
    result = {}
    # Get a list of potential targets
    targets = get_targets(entity, entity_list, target_range, entity_type = entity_type)
    # Targetting UI element
    options = [i.name for i in targets]
    menu = Menu(65, 32, 30, 15, "Target Selection", options)
    menu.render()
    terminal.refresh()
    # Menu choice
    menu_result = menu.get_choice()
    if menu_result.get("choice") is not None:
        result["target"] = targets[menu_result.get("choice")]
    elif menu_result.get("cancel"):
        result["cancel"] = True
    elif menu_result.get("quit"):
        result["quit"] = True
    return result
