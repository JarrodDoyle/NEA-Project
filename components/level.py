from components.component_base import Component
import random

class Level(Component):
    def __init__(self, base_level, base_xp, lvl_up_factor = 3, xp_drop = 0):
        self.level = base_level
        self.base_xp = base_xp
        self.level_up_xp = base_xp
        self.level_up_factor = lvl_up_factor
        self.xp = 0
        self.base_xp_drop = xp_drop

    def set_level(self, level):
        self.level = level

    def can_level_up(self):
        return self.xp >= self.level_up_xp

    def level_up(self):
        self.level += 1
        self.xp = self.xp - self.level_up_xp
        self.level_up_xp = self.base_xp * (self.level)^self.level_up_factor

    @property
    def avg_xp_drop(self):
        return self.base_xp_drop + self.level_up_factor

    def drop_xp(self):
        return random.randint(self.avg_xp_drop - self.level, self.avg_xp_drop + self.level)

    def gain_xp(self, xp):
        self.xp += xp
        message = "[color=light blue]You gain {} xp.[/color]".format(xp)
        if self.can_level_up():
            self.level_up()
            message += "\n[color=dark yellow]You leveled up! You are now level {}.[/color]".format(self.level)
        return message
