from components.component_base import Component
import dice

class Weapon(Component):
    def __init__(self, attack_power, hits):
        super().__init__()
        self.attack_power = attack_power
        self.hits = hits

    @property
    def damage(self):
        return dice.roll_dice(self.hits, self.attack_power)

class Sword(Weapon):
    def __init__(self):
        super().__init__(10, 1)
