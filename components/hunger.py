from components.component_base import Component
from game_states import Hunger_States

class Hunger(Component):
    def __init__(self, turns_to_starve, starve_damage = 1):
        self.turns_to_starve = turns_to_starve # How many turns it takes to start starving
        self.starve_damage = starve_damage # Damage taken each turn when starving
        self.turns = 0
        self.state = Hunger_States.FULL # Current hunger state

    def update(self):
        results = []
        prev_state = self.state # Store previous state for later comparison

        # If starving take damage
        if self.state == Hunger_States.STARVING:
            results.extend(self.owner.components["fighter"].take_damage(self.starve_damage))
            results.append({"message": "{} [color=red]took {} damage from starving.[/color]".format(self.owner.name, self.starve_damage)})

        if self.turns < self.turns_to_starve // 2:
            # If less than halfway to starving
            self.turns += 1
            self.state = Hunger_States.FULL
            message_state = "full"
        elif self.turns < self.turns_to_starve:
            # If over halfway towards starving
            self.turns += 1
            self.state = Hunger_States.HUNGRY
            message_state = "hungry"
        else:
            # If starving
            self.state = Hunger_States.STARVING
            message_state = "starving"

        # If hunger state changed give the player a message telling them the new state
        if self.state != prev_state:
            results.append({"message": "[color=light red]You are now {}.[/color]".format(message_state)})
        return results
