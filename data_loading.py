import shelve, os

def save_game(game):
    """
    Save the current game using a shelf
    """
    with shelve.open("save", "n") as save_file:
        save_file["game"] = game

def load_game():
    """
    Load and return a saved game in shelf format
    """
    # If save file doesn't exist raise an error
    if not os.path.isfile("save.dat"):
        raise FileNotFoundError
    # Otherwise open with shelve and initialize the new fov map
    with shelve.open("save", "r") as save_file:
        game = save_file["game"]
    game.init_fov()
    return game
