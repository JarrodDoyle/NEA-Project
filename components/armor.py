from components.component_base import Component
from random import choice, randint

class Armor(Component):
    def __init__(self, bonus_stats = {}):
        self.bonus_stats = bonus_stats
        super().__init__()

    def get_stat(self, stat):
        bonus = self.bonus_stats.get(stat)
        if bonus is not None:
            return bonus
        else:
            return 0

    def gen_random_bonus_stat(self):
        potential_stats = ["strength", "defense", "accuracy", "dexterity", "intelligence", "max_hp", None]
        stat = choice(potential_stats)
        if stat is not None:
            if self.bonus_stats.get(stat) is not None:
                self.bonus_stats[stat] += randint(1, 3)
            else:
                self.bonus_stats[stat] = randint(1, 3)
