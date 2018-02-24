from components.component_base import Component
import dice

class Melee(Component):
    def __init__(self, attack_power, hits, bonus_stats = {}):
        super().__init__()
        self.attack_power = attack_power
        self.hits = hits
        self.bonus_stats = bonus_stats

    @property
    def damage(self):
        return dice.roll_dice(self.hits, self.attack_power)

    def get_stat(self, stat):
        bonus = self.bonus_stats.get(stat)
        if bonus is not None:
            return bonus
        else:
            return 0

class Ranged(Component):
    def __init__(self):
        pass

class Wand(Component):
    def __init__(self):
        pass
