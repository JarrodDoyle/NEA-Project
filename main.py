import sys
from bearlibterminal import terminal
from initialize import initialize_terminal
from ui import Menu
from engine import Game
from data_loading import save_game, load_game

# Python recursion limit increased to allow for large cave maps
sys.setrecursionlimit(6144)

initialize_terminal()
game = None
options = ["Play game", "Load game", "Exit"]
xc, yc = 96//2, 64//2
w = 15
h = len(options)
x = xc - w//2
y = yc - h//2
main_menu = Menu(x, y, w, h, "Main Menu", options)

def play_game(game):
    playing = True
    while playing:
        result = game.play()
        if result.get("cancel") or result.get("quit"):
            playing = False
            save_game(game)
            if result.get("quit"):
                terminal.close()

while __name__ == "__main__":
    terminal.clear()
    terminal.puts(0, 0, chr(int(0xE000)))
    main_menu.render()
    terminal.refresh()
    result = main_menu.get_choice()
    if result.get("choice") == 0:
        game = Game()
        play_game(game)
    elif result.get("choice") == 1:
        try:
            game = load_game()
            play_game(game)
        except:
            pass
    elif result.get("choice") == 2 or result.get("cancel") or result.get("quit"):
        terminal.close()
        break
