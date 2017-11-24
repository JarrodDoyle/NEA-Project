def heal_entity(entity, args):
    heal_amount = args[0]
    if entity.components.get("fighter") and entity.components["fighter"].hp < entity.components["fighter"].max_hp:
        fighter = entity.components["fighter"]
        fighter.hp += heal_amount
        if fighter.hp > fighter.max_hp:
            fighter.hp = fighter.max_hp
        return True
    else:
        return False
