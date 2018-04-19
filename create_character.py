from bearlibterminal import terminal
from ui import Generic_Text_Window
import components.fighter as fighter
import re

class Character_Creation:
    """
    class used in character creation
    """
    def __init__(self):
        """
        Initialize character creation UI element
        """
        self.menu = Generic_Text_Window(1, 1, 94, 62, "Character Creation")

    def choose_name(self):
        """
        Return chosen player name
        """
        name = ""
        invalid_text = ""
        while True: # While valid name not chosen
            # Clear screen and render ui element with updated text
            terminal.clear()
            text = "Please enter your name:\n{}\n{}".format(name, invalid_text)
            self.menu.render(text)
            terminal.refresh()

            invalid_text = ""
            key = terminal.read()
            # If enter or escape is pressed
            if (key == terminal.TK_RETURN or key == terminal.TK_ESCAPE):
                # If name contains only characters of the alphabet break from loop
                # Name chosen is valid
                if re.match("^[A-Za-z]+$", name) and len(name) > 0:
                    break
                # Else tell the player their chosen name isn't valid
                else:
                    invalid_text = "That name is not valid."
            # Remove a character from the name if backspace is pressed
            elif key == terminal.TK_BACKSPACE and len(name) > 0:
                name = name[:-1]
            # Otherwise add the character of the key pressed to the name
            elif terminal.check(terminal.TK_CHAR) and len(name) < 8:
                name += chr(terminal.state(terminal.TK_CHAR))
        return name

    def choose_class(self):
        """
        Return component object of the chosen player class
        """
        # List of possible fighter class classes
        classes = [fighter.Barbarian, fighter.Wizard, fighter.Rogue, fighter.Ranger]
        # Clear screen and render ui element with updated text
        terminal.clear()
        text = "Please select a class:\n a) Barbarian:\n{}\n[color=black]█[\color]\n b) Wizard:\n{}\n[color=black]█[\color]\n c) Rogue:\n{}\n[color=black]█[\color]\n d) Ranger:\n{}".format(classes[0].description, classes[1].description, classes[2].description, classes[3].description)
        self.menu.render(text)
        terminal.refresh()

        valid_choice = False
        while not valid_choice:
            key = terminal.read()
            # If key pressed indexed from "a" is a valid index for classes list
            if key - terminal.TK_A in range(len(classes)):
                valid_choice = True
                # Get index of chosen class
                choice = key - terminal.TK_A
        return classes[choice]() # Return fighter class obejct
