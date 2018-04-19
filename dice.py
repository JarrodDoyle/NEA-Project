from random import randint

def roll_dice(number_of_dice, max_roll):
    """
    Roll an "n" sided dice "x" times and return the roll results

    number_of_dice -- how many dice to roll
    max_roll -- how many sides the dice has (maximum result of a single roll)
    """
    rolls = []

    for i in range(number_of_dice):
        rolls.append(randint(1, max_roll))

    return rolls

def mean(arr):
    """
    Return the mean value in a list
    """
    return sum(arr) / len(arr)
