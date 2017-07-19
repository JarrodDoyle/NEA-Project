class Fighter:
    # Fighter initialization
    def __init__(self, hp, strength, defense, intelligence):
        self.base_max_hp = hp
        self.hp = hp
        self.base_strength = strength
        self.base_defense = defense
        self.base_intelligence = intelligence

    # Attack another fighter
    def attack(self, target):
        results = []

        # Damage is the diffence between the fighters strength and the enemy fighters defense
        damage = self.strength - target.fighter.defense

        # If damage is greater than 0
        if damage > 0:
            # Generate appropriate attack message and simulate attack
            results.append({"message": "[color={}]{}[/color] attacked [color={}]{}[/color] for [color=red]{}[/color] hp.".format(self.owner.color, self.owner.name.capitalize(), target.color, target.name, damage)})
            results.extend(target.fighter.take_damage(damage))
        else:
            # Generate appropriate attack message
            results.append({"message": "[color={}]{}[/color] attacked [color={}]{}[/color] but did no damage.".format(self.owner.color, self.owner.name.capitalize(), target.color, target.name)})
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

    # Calculates bonus intelligence from buffs and returns it
    def bonus_intelligence(self):
        return 0

    @property
    def strength(self):
        return (self.base_strength + self.bonus_strength())

    @property
    def defense(self):
        return (self.base_defense + self.bonus_defense())

    @property
    def intelligence(self):
        return (self.base_intelligence + self.bonus_intelligence())

    @property
    def max_hp(self):
        return self.base_max_hp
