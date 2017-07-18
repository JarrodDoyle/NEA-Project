import libtcodpy as libtcod
from components import *

class Entity:
    def __init__(self, x, y, name, char, color):
        self.x = x
        self.y = y
        self.name = name
        self.char = char
        self.color = color
        self.inventory = []
        self.messages = []

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "Player", "@", "white")
        self.fighter = Fighter(hp = 100, strength = 4, defense = 1, intelligence = 0)

    def move_or_attack(self, level, dx, dy, ui_elements):
        x = self.x + dx
        y = self.y + dy
        if level[y][x].is_blocked == False:
            entity = level[y][x].entity
            if entity is not None:
                self.fighter.attack(entity)
                ui_elements["player"].redraw = True
            else:
                self.move(level, dx, dy)


    def move(self, level, dx, dy):
        level[self.y][self.x].remove_entity()
        self.x += dx
        self.y += dy
        self.x_offset -= dx
        self.y_offset -= dy
        level[self.y][self.x].add_entity(self)

class Goblin(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "goblin", "g", "green")
        self.fighter = Fighter(hp = 30, strength = 3, defense = 0, intelligence = 0)

def get_visible_entities(player, entities, fov_map):
    visible_entities = []
    for entity in entities:
        if entity != player:
            visible = libtcod.map_is_in_fov(fov_map, entity.x, entity.y)
            if visible:
                visible_entities.append(entity)
    return visible_entities
