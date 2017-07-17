class Fighter:
    def __init__(self, hp, strength, defense, intelligence):
        self.base_max_hp = hp
        self.hp = hp
        self.base_strength = strength
        self.base_defense = defense
        self.base_intelligence = intelligence

    def attack(self, target):
        damage = self.strength - target.fighter.defense
        if damage > 0:
            target.fighter.hp -= damage
        else:
            print("shit son no damage")

    def bonus_strength(self):
        return 0

    def bonus_defense(self):
        return 0

    def bonus_intelligence(self):
        return 0

    @property
    def strength(self):
        return self.base_strength

    @property
    def defense(self):
        return self.base_defense

    @property
    def intelligence(self):
        return self.base_intelligence

    @property
    def max_hp(self):
        return self.base_max_hp
