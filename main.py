from bearlibterminal import terminal
from initialize import initialize_terminal
from play_game import Game

initialize_terminal()
game = None

while True:
    terminal.clear()
    terminal.puts(0, 0, chr(int(0xE000)))
    options = ["Play game", "Options", "Exit"]
    x, y = 40, 32
    letter_index = ord("a")
    for i in options:
        terminal.puts(x, y, "{}) {}".format(chr(letter_index), i))
        letter_index += 1
        y += 1
    terminal.refresh()
    choice = terminal.read()
    if choice == terminal.TK_A:
        game = Game()
        playing = True
        while playing:
            playing = game.play()
    elif choice == terminal.TK_B:
        options = True
    elif choice == terminal.TK_C:         
        terminal.close()
        break
