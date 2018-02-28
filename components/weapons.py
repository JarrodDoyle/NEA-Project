from components.component_base import Component
from random import choice, randint
import dice

# Base weapon component inherited by all weapon types
class Weapon(Component):
    def __init__(self, attack_power, attack_range, hits, weapon_type, bonus_stats = {}):
        super().__init__()
        self.attack_power = attack_power
        self.attack_range = attack_range
        self.hits = hits
        self.bonus_stats = bonus_stats

    def get_damage_roll(self, affecting_stat):
        max_hit_damage = int(self.attack_power * (affecting_stat / 4))
        return dice.roll_dice(self.hits, max_hit_damage)

    def gen_random_bonus_stat(self):
        # Choose a random stat to increase by a random amount
        potential_stats = ["strength", "defense", "accuracy", "dexterity", "intelligence", None]
        stat = choice(potential_stats)
        if stat is not None:
            if self.bonus_stats.get(stat) is not None:
                self.bonus_stats[stat] += randint(1, 2)
            else:
                self.bonus_stats[stat] = randint(1, 2)
            print(stat, self.bonus_stats[stat])

    def get_stat(self, stat):
        bonus = self.bonus_stats.get(stat)
        if bonus is not None:
            return bonus
        else:
            return 0

class Melee(Weapon):
    def __init__(self, attack_power, hits, attack_range = 1, bonus_stats = {}):
        super().__init__(attack_power, attack_range, hits, "melee", bonus_stats)

    # Melee weapons simply do a damage roll
    def damage(self, fighter):
        return self.get_damage_roll(fighter.strength)

class Ranged(Weapon):
    def __init__(self, attack_power, hits, attack_range, bonus_stats = {}):
        super().__init__(attack_power, attack_range, hits, "ranged", bonus_stats)

    # If the entity using the weapon has arrows do a damage roll and reduce their arrow count
    def damage(self, fighter):
        equipment_component = fighter.owner.components.get("equipment")
        if equipment_component is not None:
            if equipment_component.equipment["arrows"] > 0:
                damage = self.get_damage_roll(fighter.dexterity)
                equipment_component.equipment["arrows"] -= self.hits
            else:
                damage = []
        else:
            damage = []
        return damage

class Wand(Weapon):
    def __init__(self, attack_power, hits, attack_range, charges, bonus_stats = {}):
        self.charges = charges
        super().__init__(attack_power, attack_range, hits, "wand", bonus_stats)

    # If the wand still has charges, do a damage roll and reduce the charges by 1
    def damage(self, fighter):
        if self.charges > 0:
            self.charges -= 1
            damage = self.get_damage_roll(fighter.intelligence)
        else:
            damage = []
        return damage
