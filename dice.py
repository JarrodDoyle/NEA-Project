from random import randint

def roll_dice(number_of_dice, max_roll):
    # rolls an n sided dice x times and returns the results
    rolls = []

    for i in range(number_of_dice):
        rolls.append(randint(1, max_roll))

    return rolls

def mean(arr):
    return sum(arr) / len(arr)
