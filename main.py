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
main_menu = Menu(x, y, w, h, "Main Menu", options, "black")


while True:
    terminal.clear()
    terminal.puts(0, 0, chr(int(0xE000)))
    main_menu.render()
    terminal.refresh()
    choice = main_menu.get_choice()
    if choice == 0:
        game = Game()
        playing = True
        while playing:
            playing = game.play()
    elif choice == 1:
        pass
    elif choice == 2:
        terminal.close()
        break
