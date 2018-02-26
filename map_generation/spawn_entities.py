import entities.mobs as mobs
import entities.items as items
import dice
from random import choice
from inspect import getmembers, isclass

def choose_entity_to_spawn(entity_type):
    if entity_type == "item":
        arr = get_item_list()
    elif entity_type == "mob":
        arr = get_mob_list()

    weight_sum = 0
    for i in arr:
        weight_sum += i[1]

    roll = dice.roll_dice(1, weight_sum)[0]
    chance_sum = 0
    for i in range(len(arr)):
        chance_sum += arr[i][1]
        if chance_sum >= roll:
            entity = arr[i][0]
            break
    return entity

def get_mob_list():
    return [[mobs.Mob_Goblin, mobs.Mob_Goblin.spawn_weight],
            [mobs.Mob_Ant, mobs.Mob_Ant.spawn_weight],
            [mobs.Mob_Blob, mobs.Mob_Blob.spawn_weight],
            [mobs.Mob_Cockatrice, mobs.Mob_Cockatrice.spawn_weight],
            [mobs.Mob_Wolf, mobs.Mob_Wolf.spawn_weight],
            [mobs.Mob_Floating_Eye, mobs.Mob_Floating_Eye.spawn_weight],
            [mobs.Mob_Feral_Cat, mobs.Mob_Feral_Cat.spawn_weight],
            [mobs.Mob_Gremlin, mobs.Mob_Gremlin.spawn_weight],
            [mobs.Mob_Hobbit, mobs.Mob_Hobbit.spawn_weight],
            [mobs.Mob_Imp, mobs.Mob_Imp.spawn_weight],
            [mobs.Mob_Kobold, mobs.Mob_Kobold.spawn_weight],
            [mobs.Mob_Nymph, mobs.Mob_Nymph.spawn_weight],
            [mobs.Mob_Orc, mobs.Mob_Orc.spawn_weight],
            [mobs.Mob_Giant_Rat, mobs.Mob_Giant_Rat.spawn_weight],
            [mobs.Mob_Cave_Spider, mobs.Mob_Cave_Spider.spawn_weight],
            [mobs.Mob_Horse, mobs.Mob_Horse.spawn_weight],
            [mobs.Mob_Worm, mobs.Mob_Worm.spawn_weight],
            [mobs.Mob_Bat, mobs.Mob_Bat.spawn_weight],
            [mobs.Mob_Centaur, mobs.Mob_Bat.spawn_weight],
            [mobs.Mob_Dragon, mobs.Mob_Dragon.spawn_weight],
            [mobs.Mob_Gnome, mobs.Mob_Gnome.spawn_weight],
            [mobs.Mob_Giant, mobs.Mob_Giant.spawn_weight],
            [mobs.Mob_Lich, mobs.Mob_Lich.spawn_weight],
            [mobs.Mob_Naga, mobs.Mob_Naga.spawn_weight],
            [mobs.Mob_Ogre, mobs.Mob_Ogre.spawn_weight],
            [mobs.Mob_Snake, mobs.Mob_Snake.spawn_weight],
            [mobs.Mob_Monkey, mobs.Mob_Monkey.spawn_weight]]

def get_item_list():
    return [[items.Test_Wand, items.Test_Wand.spawn_weight],
            [items.Iron_Longsword, items.Iron_Longsword.spawn_weight],
            [items.Copper_Longsword, items.Copper_Longsword.spawn_weight],
            [items.Battle_Axe, items.Battle_Axe.spawn_weight],
            [items.Iron_Axe, items.Iron_Axe.spawn_weight],
            [items.Copper_Axe, items.Copper_Axe.spawn_weight],
            [items.Copper_Sword, items.Copper_Sword.spawn_weight],
            [items.Iron_Sword, items.Iron_Sword.spawn_weight],
            [items.Copper_Dagger, items.Copper_Dagger.spawn_weight],
            [items.Iron_Dagger, items.Iron_Dagger.spawn_weight],
            [items.Health_Potion, items.Health_Potion.spawn_weight],
            [items.Strength_Potion, items.Strength_Potion.spawn_weight],
            [items.Defense_Potion, items.Defense_Potion.spawn_weight],
            [items.Accuracy_Potion, items.Accuracy_Potion.spawn_weight],
            [items.Intelligence_Potion, items.Intelligence_Potion.spawn_weight],
            [items.Dexterity_Potion, items.Dexterity_Potion.spawn_weight],
            [items.Max_HP_Potion, items.Max_HP_Potion.spawn_weight]]
