from random import randint

def roll_dice(number_of_dice, max_roll):
    rolls = []

    for i in range(number_of_dice):
        rolls.append(randint(1, max_roll))

    return rolls

def mean(arr):
    return sum(arr) / len(arr)

if __name__ == "__main__":
    while True:
        num_dice = int(input("How many dice: "))
        #num_sides = int(input("How many sides of dice: "))
        num_sides = 6
        results = roll_dice(num_dice, num_sides)
        print(mean(results))
        input()
