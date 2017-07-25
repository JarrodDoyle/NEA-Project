from random import randint

def roll_dice(number_of_dice, max_roll):
    rolls = []

    for i in range(number_of_dice):
        roll = randint(1, max_roll)
        rolls.append(roll)

    return rolls
