def heal_entity(entity, args):
    heal_amount = args.get("heal_amount")
    if entity.components.get("fighter") and entity.components["fighter"].hp < entity.components["fighter"].max_hp:
        fighter = entity.components["fighter"]
        fighter.hp += heal_amount
        if fighter.hp > fighter.max_hp:
            fighter.hp = fighter.max_hp
        return True
    else:
        return False

def damage_entity(entity, args):
    args = {"heal_amount": args.get("damage_amount")}
    return heal_entity(entity, args)
