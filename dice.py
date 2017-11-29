from random import randint

def roll_dice(number_of_dice, max_roll):
    rolls = []

    for i in range(number_of_dice):
        rolls.append(randint(1, max_roll))

    return rolls

def mean(arr):
    return sum(arr) / len(arr)
