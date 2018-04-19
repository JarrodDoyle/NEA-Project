import sys
from bearlibterminal import terminal
from initialize import initialize_terminal
from ui import Menu
from engine import Game
from data_loading import save_game, load_game

# Python recursion limit increased to allow for large cave maps
sys.setrecursionlimit(6144)

# Initialize BearLibTerminal termianl
initialize_terminal()

# Main menu UI element creation
options = ["Play game", "Load game", "Exit"]
xc, yc = 96//2, 64//2
w = 15
h = len(options)
x = xc - w//2
y = yc - h//2
main_menu = Menu(x, y, w, h, "Main Menu", options)

def play_game(game):
    """
    Play the game

    game -- Game object to play
    """
    while True:
        result = game.play() # dict returned by game object each turn
        if result.get("cancel") or result.get("quit"):
            # Always save game whether exiting to main menu or quitting entirely
            save_game(game)
            if result.get("quit"):
                terminal.close()
            break

while __name__ == "__main__":
    # While loop holds the main menu
    # Menu rendering block
    terminal.clear()
    terminal.puts(0, 0, chr(int(0xE000)))
    main_menu.render()
    terminal.refresh()

    # Menu selection block
    result = main_menu.get_choice()
    # If player wants to play a new game create a new game object and play it
    if result.get("choice") == 0:
        game = Game()
        play_game(game)
    # If player wants to load a previously saved game
    elif result.get("choice") == 1:
        # Attempt to load a game but do nothing if no game is found/game is corrupted
        try:
            game = load_game()
            play_game(game)
        except:
            pass
    # Otherwise quit the game
    elif result.get("choice") == 2 or result.get("cancel") or result.get("quit"):
        terminal.close()
        break
