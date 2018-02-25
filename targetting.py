from ui import Menu
from bearlibterminal import terminal

def get_targets(entity, entity_list, target_range, entity_type = None):
    targets = []
    for other_entity in entity_list:
        if entity_type is None:
            if other_entity != entity and entity.distance_to(other_entity) < target_range + 1:
                targets.append(other_entity)
        else:
            if other_entity != entity and other_entity.components.get(entity_type) and entity.distance_to(other_entity) < target_range + 1:
                targets.append(other_entity)
    return targets

def choose_target(entity, entity_list, target_range, entity_type = None):
    result = {}
    targets = get_targets(entity, entity_list, target_range, entity_type = entity_type)
    options = [i.name for i in targets]
    menu = Menu(65, 32, 30, 15, "Target Selection", options)
    menu.render()
    terminal.refresh()
    menu_result = menu.get_choice()
    if menu_result.get("choice") is not None:
        result["target"] = targets[menu_result.get("choice")]
    elif menu_result.get("cancel"):
        result["cancel"] = True
    elif menu_result.get("quit"):
        result["quit"] = True
    return result
