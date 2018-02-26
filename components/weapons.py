from components.component_base import Component
from random import choice, randint
import dice

class Weapon(Component):
    def __init__(self, attack_power, attack_range, hits, bonus_stats = {}):
        super().__init__()
        self.attack_power = attack_power
        self.attack_range = attack_range
        self.hits = hits
        self.bonus_stats = bonus_stats

    def get_damage_roll(self, affecting_stat):
        max_hit_damage = int(self.attack_power * (affecting_stat / 4))
        return dice.roll_dice(self.hits, max_hit_damage)

    def gen_random_bonus_stat(self):
        potential_stats = ["strength", "defense", "accuracy", "dexterity", "intelligence", "max_hp", None]
        stat = choice(potential_stats)
        if stat is not None:
            if self.bonus_stats.get(stat) is not None:
                self.bonus_stats[stat] += randint(1, 3)
            else:
                self.bonus_stats[stat] = randint(1, 3)
            print(stat, self.bonus_stats[stat])

    def get_stat(self, stat):
        bonus = self.bonus_stats.get(stat)
        if bonus is not None:
            return bonus
        else:
            return 0

class Melee(Weapon):
    def __init__(self, attack_power, hits, attack_range = 1, bonus_stats = {}):
        super().__init__(attack_power, attack_range, hits, bonus_stats)

    def damage(self, fighter):
        return self.get_damage_roll(fighter.strength)

class Ranged(Weapon):
    def __init__(self, attack_power, hits, attack_range, bonus_stats = {}):
        super().__init__(attack_power, attack_range, hits, bonus_stats)

    def damage(self, fighter):
        return self.get_damage_roll(fighter.dexterity)

class Wand(Weapon):
    def __init__(self, attack_power, hits, attack_range, bonus_stats = {}):
        super().__init__(attack_power, attack_range, hits, bonus_stats)

    def damage(self, fighter):
        return self.get_damage_roll(fighter.intelligence)
