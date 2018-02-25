import shelve, os

def save_game(game):
    with shelve.open("save", "n") as save_file:
        save_file["game"] = game

def load_game():
    if not os.path.isfile("save.dat"):
        raise FileNotFoundError
    with shelve.open("save", "r") as save_file:
        game = save_file["game"]
    return game
