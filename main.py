import sys
from bearlibterminal import terminal
from initialize import initialize_terminal
from ui import Menu
from play_game import Game

sys.setrecursionlimit(6144)

initialize_terminal()
game = None
options = ["Play game", "Options", "Exit"]
xc, yc = 96//2, 64//2
w = 15
h = len(options)
x = xc - w//2
y = yc - h//2
main_menu = Menu(x, y, w, h, "Main Menu", options)

while True:
    terminal.clear()
    terminal.puts(0, 0, chr(int(0xE000)))
    main_menu.render()
    terminal.refresh()
    result = main_menu.get_choice()
    if result.get("choice") == 0:
        game = Game()
        playing = True
        while playing:
            result = game.play()
            if result.get("cancel") or result.get("quit"):
                playing = False
                if result.get("quit"):
                    terminal.close()
    elif result.get("choice") == 1:
        pass
    elif result.get("choice") == 2 or result.get("cancel") or result.get("quit"):
        terminal.close()
        break
