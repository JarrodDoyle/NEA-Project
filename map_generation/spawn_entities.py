import entities.mobs as mobs
import entities.items as items
import dice
from random import choice
from inspect import getmembers, isclass

def get_mob_list():
    mob_list = [mobs.Mob_Goblin, mobs.Mob_Ant, mobs.Mob_Blob, mobs.Mob_Cockatrice, mobs.Mob_Wolf, mobs.Mob_Floating_Eye, mobs.Mob_Feral_Cat, mobs.Mob_Gremlin, mobs.Mob_Hobbit, mobs.Mob_Imp, mobs.Mob_Kobold, mobs.Mob_Nymph, mobs.Mob_Orc, mobs.Mob_Giant_Rat, mobs.Mob_Cave_Spider, mobs.Mob_Horse, mobs.Mob_Worm, mobs.Mob_Bat, mobs.Mob_Centaur, mobs.Mob_Dragon, mobs.Mob_Gnome, mobs.Mob_Giant, mobs.Mob_Lich, mobs.Mob_Naga, mobs.Mob_Ogre, mobs.Mob_Snake, mobs.Mob_Monkey]
    #mob_list = [list(i[1][-len(i[0]):-3] for i in getmembers(mobs, isclass) if i[0][:3] == "Mob"]
    #mob_list = getmembers(mobs, isclass)
    #print(mob_list[0][0][:3])
    return mob_list

def get_item_list():
    item_list = [items.Health_Pot]
    return item_list

def choose_item_to_spawn():
    potential_items = get_item_list()
    item_spawned = False
    while not item_spawned:
        item = choice(potential_items)
        roll = dice.roll_dice(1, 100)[0]
        item_spawned = [0,1][roll <= item(0,0).components["item"].spawn_chance]
    return item

def choose_mob_to_spawn():
    potential_mobs = get_mob_list()
    mob_spawned = False
    while not mob_spawned:
        mob = choice(potential_mobs)
        roll = dice.roll_dice(1, 100)[0]
        mob_spawned = [0,1][roll <= mob(0,0).components["fighter"].spawn_chance]
    return mob
