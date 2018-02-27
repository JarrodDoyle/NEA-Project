from bearlibterminal import terminal
from ui import Generic_Text_Window
import components.fighter as fighter

class Character_Creation:
    def choose_name(self):
        name = ""
        menu = Generic_Text_Window(1, 1, 94, 62, "Character Creation")
        while True:
            terminal.clear()
            text = "Please enter your name:\n{}".format(name)
            menu.render(text)
            terminal.refresh()
            key = terminal.read()

            if (key == terminal.TK_RETURN or key == terminal.TK_ESCAPE) and len(name) > 0:
                break
            elif key == terminal.TK_BACKSPACE and len(name) > 0:
                name = name[:-1]
            elif terminal.check(terminal.TK_CHAR) and len(name) < 8:
                name += chr(terminal.state(terminal.TK_CHAR))
        return name

    def choose_class(self):
        menu = Generic_Text_Window(1, 1, 94, 62, "Character Creation")
        classes = [fighter.Barbarian, fighter.Wizard, fighter.Rogue, fighter.Ranger, fighter.God]
        text = "Please select a class:\n a) Barbarian\n b) Wizard\n c) Rogue\n d) Ranger\n e) GOD"
        menu.render(text)
        terminal.refresh()
        valid_choice = False
        while not valid_choice:
            key = terminal.read()
            if key - terminal.TK_A in range(len(classes)):
                valid_choice = True
                choice = key - terminal.TK_A
        return classes[choice]()
