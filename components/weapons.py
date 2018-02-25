from components.component_base import Component
import dice

class Weapon(Component):
    def __init__(self, attack_power, hits, bonus_stats = {}):
        super().__init__()
        self.attack_power = attack_power
        self.hits = hits
        self.bonus_stats = bonus_stats

    def get_damage_roll(self, affecting_stat):
        max_hit_damage = int(self.attack_power * (affecting_stat / 4))
        return dice.roll_dice(self.hits, max_hit_damage)

    def get_stat(self, stat):
        bonus = self.bonus_stats.get(stat)
        if bonus is not None:
            return bonus
        else:
            return 0

class Melee(Weapon):
    def __init__(self, attack_power, hits, bonus_stats = {}):
        super().__init__(attack_power, hits, bonus_stats)

    def damage(self, fighter):
        return self.get_damage_roll(fighter.strength)

class Ranged(Weapon):
    def __init__(self, attack_power, hits, bonus_stats = {}):
        super().__init__(attack_power, hits, bonus_stats)

    def damage(self, fighter):
        return self.get_damage_roll(fighter.dexterity)

class Wand(Weapon):
    def __init__(self, attack_power, hits, bonus_stats = {}):
        super().__init__(attack_power, hits, bonus_stats)

    def damage(self, fighter):
        return self.get_damage_roll(fighter.intelligence)
