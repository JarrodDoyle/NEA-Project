from dice import roll_dice
from components.component_base import Component
import random

class Fighter(Component):
    # Fighter initialization
    def __init__(self, hp, strength, defense, accuracy, intelligence):
        super().__init__()
        self.base_max_hp = hp
        self.hp = hp
        self.base_strength = strength
        self.base_defense = defense
        self.base_accuracy = accuracy
        self.base_intelligence = intelligence

    # Attack another fighter
    def attack(self, target):
        results = []

        attacker_accuracy = roll_dice(1, self.accuracy)
        target_defense = roll_dice(1, target.components["fighter"].defense)
        if attacker_accuracy > target_defense:
            weapon1 = self.owner.components.get("equipment").equipment.get("l_hand")
            if weapon1 == None:
                weapon1_damage = 0
            else:
                weapon1_damage = weapon1.damage

            weapon2 = self.owner.components.get("equipment").equipment.get("r_hand")
            if weapon2 == None:
                weapon2_damage = 0
            else:
                weapon2_damage = weapon2.damage

            # Damage is the diffence between the fighters strength and the enemy fighters defense
            damage = random.randint(self.strength // 2, self.strength) + weapon1_damage + weapon2_damage

            # Generate appropriate attack message and simulate attack
            results.append({"message": "[color={}]{}[color=red] dealt {} damage to [color={}]{}[color=red].".format(self.owner.color, self.owner.name.capitalize(), damage, target.color, target.name)})
            results.extend(target.components["fighter"].take_damage(damage))
        else:
            results.append({"message": "[color={}]{}'s[/color] attack missed".format(self.owner.color, self.owner.name.capitalize())})
        return results

    # Take damage
    def take_damage(self, damage):
        results = []

        # Take the damage
        self.hp -= damage

        # If fighter is dead return result saying so
        if self.hp <= 0:
            results.append({"dead": self.owner})
        return results

    # Calculates bonus strength from weapons and buffs and returns it
    def bonus_strength(self):
        return 0

    # Calculates bonus defense from amor and buffs and returns it
    def bonus_defense(self):
        return 0

    def bonus_accuracy(self):
        return 0

    # Calculates bonus intelligence from buffs and returns it
    def bonus_intelligence(self):
        return 0

    @property
    def strength(self):
        return (self.base_strength + self.bonus_strength())

    @strength.setter
    def strength(self, value):
        self.base_strength = value

    @property
    def defense(self):
        return (self.base_defense + self.bonus_defense())

    @defense.setter
    def defense(self, defense):
        self.base_defense = defense

    @property
    def accuracy(self):
        return (self.base_accuracy + self.bonus_accuracy())

    @accuracy.setter
    def accuracy(self, accuracy):
        self.base_accuracy = accuracy

    @property
    def intelligence(self):
        return (self.base_intelligence + self.bonus_intelligence())

    @intelligence.setter
    def intelligence(self, intelligence):
        self.base_intelligence = intelligence

    @property
    def max_hp(self):
        return self.base_max_hp

    @max_hp.setter
    def max_hp(self, hp):
        self.base_max_hp = hp
