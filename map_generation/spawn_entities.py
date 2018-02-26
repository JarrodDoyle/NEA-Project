import entities.mobs as mobs
import entities.items as items
import dice
from random import choice
from inspect import getmembers, isclass

def choose_entity_to_spawn(entity_type, floor_index):
    if entity_type == "item":
        arr = get_item_list()
    elif entity_type == "mob":
        arr = get_mob_list()

    weight_sum = 0
    for i in arr:
        weight_sum += max(i.base_spawn_weight * (floor_index - i.lowest_level_spawn + 1), 0)

    roll = dice.roll_dice(1, weight_sum)[0]
    chance_sum = 0
    for entity in arr:
        chance_sum += max(entity.base_spawn_weight * (floor_index - entity.lowest_level_spawn + 1), 0)
        if chance_sum >= roll:
            break
    return entity

def get_mob_list():
    return [mobs.Mob_Goblin,
            mobs.Mob_Ant,
            mobs.Mob_Blob,
            mobs.Mob_Cockatrice,
            mobs.Mob_Wolf,
            mobs.Mob_Floating_Eye,
            mobs.Mob_Feral_Cat,
            mobs.Mob_Gremlin,
            mobs.Mob_Hobbit,
            mobs.Mob_Imp,
            mobs.Mob_Kobold,
            mobs.Mob_Nymph,
            mobs.Mob_Orc,
            mobs.Mob_Giant_Rat,
            mobs.Mob_Cave_Spider,
            mobs.Mob_Horse,
            mobs.Mob_Worm,
            mobs.Mob_Bat,
            mobs.Mob_Centaur,
            mobs.Mob_Dragon,
            mobs.Mob_Gnome,
            mobs.Mob_Giant,
            mobs.Mob_Lich,
            mobs.Mob_Naga,
            mobs.Mob_Ogre,
            mobs.Mob_Snake,
            mobs.Mob_Monkey]

def get_item_list():
    return [items.Test_Wand,
            items.Iron_Longsword,
            items.Copper_Longsword,
            items.Battle_Axe,
            items.Iron_Axe,
            items.Copper_Axe,
            items.Copper_Sword,
            items.Iron_Sword,
            items.Copper_Dagger,
            items.Iron_Dagger,
            items.Health_Potion,
            items.Strength_Potion,
            items.Defense_Potion,
            items.Accuracy_Potion,
            items.Intelligence_Potion,
            items.Dexterity_Potion,
            items.Max_HP_Potion,
            items.Weak_Food,
            items.Strong_Food,
            items.Leather_Helmet]
