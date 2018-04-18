from components.component_base import Component
from ui import Generic_Text_Window
from bearlibterminal import terminal
import random

class Level(Component):
    """
    Level component inheriting from Component
    """
    def __init__(self, base_level, base_xp, lvl_up_factor = 3, xp_drop = 0):
        """
        Initialize level component

        base_level -- level to start at
        base_xp -- base xp needed to level up
        lvl_up_factor -- used as a power when calculating xp needed to progress
        a level.
        xp_drop -- how much xp to drop on death
        """
        self.level = base_level
        self.base_xp = base_xp
        self.level_up_xp = base_xp
        self.level_up_factor = lvl_up_factor
        self.xp = 0
        self.base_xp_drop = xp_drop

    def set_level(self, level):
        """
        Set the level
        """
        self.level = level

    def can_level_up(self):
        """
        Return a boolean value representing whether the entity can level up
        """
        return self.xp >= self.level_up_xp

    def level_up(self):
        """
        Level up the entity.
        """
        # Create a level up window
        menu = Generic_Text_Window(1, 1, 94, 62, "Level Up Menu")
        self.level += 1
        self.xp = self.xp - self.level_up_xp
        self.level_up_xp = self.base_xp * (self.level)^self.level_up_factor

        fighter = self.owner.components.get("fighter")

        # Text for level up window
        confirmed_stats = False
        while not confirmed_stats:
            available_points = 5
            stats = [0, 0, 0, 0, 0, 0]
            while available_points > 0:
                terminal.clear()
                text = "Chose stats to increase, you have {} points remaining:".format(available_points)
                text += "\n a) Strength: {} (+{})".format(fighter.strength, stats[0])
                text += "\n b) Defense: {} (+{})".format(fighter.defense, stats[1])
                text += "\n c) Accuracy: {} (+{})".format(fighter.accuracy, stats[2])
                text += "\n d) Intelligence: {} (+{})".format(fighter.intelligence, stats[3])
                text += "\n e) Dexterity: {} (+{})".format(fighter.dexterity, stats[4])
                text += "\n f) Max HP: {} (+{})".format(fighter.max_hp, stats[5] * 5)
                menu.render(text)
                terminal.refresh()
                valid_choice = False
                while not valid_choice:
                    key = terminal.read()
                    if key - terminal.TK_A in range(len(stats)):
                        valid_choice = True
                        choice = key - terminal.TK_A
                stats[choice] += 1
                available_points -= 1
            terminal.clear()
            text = "Press 'a' to confirm the following stat changes or 'b' to reset them:"
            text += "\n a) Strength: {} (+{})".format(fighter.strength, stats[0])
            text += "\n b) Defense: {} (+{})".format(fighter.defense, stats[1])
            text += "\n c) Accuracy: {} (+{})".format(fighter.accuracy, stats[2])
            text += "\n d) Intelligence: {} (+{})".format(fighter.intelligence, stats[3])
            text += "\n e) Dexterity: {} (+{})".format(fighter.dexterity, stats[4])
            text += "\n f) Max HP: {} (+{})".format(fighter.max_hp, stats[5] * 5)
            menu.render(text)
            terminal.refresh()
            valid_choice = False
            while not valid_choice:
                key = terminal.read()
                if key - terminal.TK_A in range(2):
                    valid_choice = True
                    confirmed_stats = not (key - terminal.TK_A)

        # Increase fighter stats by chosen amount
        fighter.strength += stats[0]
        fighter.defense += stats[1]
        fighter.accuracy += stats[2]
        fighter.intelligence += stats[3]
        fighter.dexterity += stats[4]
        fighter.max_hp += stats[5] * 5

    @property
    def avg_xp_drop(self):
        return self.base_xp_drop + self.level_up_factor

    def drop_xp(self):
        """
        Returns how much xp to drop.
        """
        return random.randint(self.avg_xp_drop - self.level, self.avg_xp_drop + self.level)

    def gain_xp(self, xp):
        """
        Gain xp and return the results.

        xp -- how much xp to gain.
        """
        results = []
        self.xp += xp
        results.append({"message": "[color=light blue]You gain {} xp.[/color]".format(xp)})
        if self.can_level_up():
            self.level_up()
            results.append({"message": "[color=dark yellow]You leveled up! You are now level {}.[/color]".format(self.level)})
        return results
