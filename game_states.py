from enum import Enum

class Game_States(Enum):
    PLAYER_TURN = 1
    ENEMY_TURN = 2
    PLAYER_DEAD = 3
    INVENTORY_ACTIVE = 4
    USING_ITEM = 5
    WIN = 6

class Hunger_States(Enum):
    STARVING = 1
    HUNGRY = 2
    FULL = 3
