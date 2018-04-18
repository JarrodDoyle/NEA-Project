from components.component_base import Component
from random import choice, randint

class Armor(Component):
    """
    Armor component inheriting from Component
    """
    def __init__(self, bonus_stats = {}):
        """
        Initialize armor component.

        bonus_stats -- Dictionary detailing bonus stats provided by the armor,
        defaults to an empty dict.
        """
        self.bonus_stats = bonus_stats
        super().__init__()

    def get_stat(self, stat):
        """
        Return the amount of a specified stat that the armor provides.
        """
        bonus = self.bonus_stats.get(stat)
        if bonus is not None:
            return bonus
        else:
            return 0

    def gen_random_bonus_stat(self):
        """
        Generate a random bonus stat for the armor.
        """
        # Picks a random stat from the list
        potential_stats = ["strength", "defense", "accuracy", "dexterity", "intelligence", "max_hp", None]
        stat = choice(potential_stats)
        if stat is not None:
            # If self already increases the specified stat, sum the bonuses
            if self.bonus_stats.get(stat) is not None:
                self.bonus_stats[stat] += randint(1, 3)
            # Else add the stat and amount to the bonus stat dict
            else:
                self.bonus_stats[stat] = randint(1, 3)
