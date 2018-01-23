from bearlibterminal import terminal
from ui import UI_Element

class Character_Creation:   
    def choose_name(self, character_creation_ui):
        name = ""
        while True:
            character_creation_ui.render(name)
            terminal.refresh()
            key = terminal.read()

            if key == terminal.TK_RETURN or key == terminal.TK_ESCAPE:
                break
            elif key == terminal.TK_BACKSPACE and len(name) > 0:
                name = name[:-1]
            elif terminal.check(terminal.TK_CHAR) and len(name) < 8:
                name += chr(terminal.state(terminal.TK_CHAR))

            terminal.puts(character_creation_ui.x, character_creation_ui.y, name)
        return name
