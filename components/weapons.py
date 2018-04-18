from components.component_base import Component
from random import choice, randint
import dice

class Weapon(Component):
    """
    Weapon component to be inherited by all weapons, inherits from Component.
    """
    def __init__(self, attack_power, attack_range, hits, weapon_type, bonus_stats = {}):
        """
        Initialize weapon component

        attack_power -- base weapon damage
        attack_range -- how many cells the weapon can attack from
        hits -- how many hits the weapon does
        weapon_type -- melee/ranged/wand
        bonus_stats -- fighter stats provided by the weapon
        """
        super().__init__()
        self.attack_power = attack_power
        self.attack_range = attack_range
        self.hits = hits
        self.bonus_stats = bonus_stats

    def get_damage_roll(self, affecting_stat):
        """
        Return list of dice rolls for damage

        affecting_stat -- the name of the stat that affects the weapons damage
        """
        max_hit_damage = int(self.attack_power * (affecting_stat / 4))
        return dice.roll_dice(self.hits, max_hit_damage)

    def gen_random_bonus_stat(self):
        """
        Generate a random bonus stat for the weapon.
        """
        potential_stats = ["strength", "defense", "accuracy", "dexterity", "intelligence", None]
        stat = choice(potential_stats)
        if stat is not None:
            if self.bonus_stats.get(stat) is not None:
                self.bonus_stats[stat] += randint(1, 2)
            else:
                self.bonus_stats[stat] = randint(1, 2)

    def get_stat(self, stat):
        """
        Return the amount of a specified stat provided by the weapon
        """
        bonus = self.bonus_stats.get(stat)
        if bonus is not None:
            return bonus
        else:
            return 0

class Melee(Weapon):
    """
    Base melee weapon class to be inherited by melee weapons, inherits from
    Weapon
    """
    def __init__(self, attack_power, hits, attack_range = 1, bonus_stats = {}):
        """
        Initialize melee weapon
        """
        super().__init__(attack_power, attack_range, hits, "melee", bonus_stats)

    def damage(self, fighter):
        """
        Return the result of dice rolls for damage
        """
        return self.get_damage_roll(fighter.strength)

class Ranged(Weapon):
    """
    Base ranged weapon class to be inherited by ranged weapons, inherits from Weapon
    """
    def __init__(self, attack_power, hits, attack_range, bonus_stats = {}):
        """
        Initialize ranged weapon
        """
        super().__init__(attack_power, attack_range, hits, "ranged", bonus_stats)

    # If the entity using the weapon has arrows do a damage roll and reduce their arrow count
    def damage(self, fighter):
        """
        Return weapon damage
        """
        equipment_component = fighter.owner.components.get("equipment")
        # If the entity has an equipment component
        if equipment_component is not None:
            # If entity has ammo
            if equipment_component.equipment["arrows"] > 0:
                # Do damage rolls and reduce ammo count appropriately
                damage = self.get_damage_roll(fighter.dexterity)
                equipment_component.equipment["arrows"] -= self.hits
            else:
                damage = []
        else:
            damage = []
        return damage

class Wand(Weapon):
    """
    Base wand classs to be inherited by wands, inherits from Weapon
    """
    def __init__(self, attack_power, hits, attack_range, charges, bonus_stats = {}):
        """
        Initialize wand
        """
        self.charges = charges
        super().__init__(attack_power, attack_range, hits, "wand", bonus_stats)

    def damage(self, fighter):
        """
        Return weapon damage
        """
        # If the wand still has charges, do a damage roll and reduce the charges.
        if self.charges > 0:
            self.charges -= 1
            damage = self.get_damage_roll(fighter.intelligence)
        else:
            damage = []
        return damage
