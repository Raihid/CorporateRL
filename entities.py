import random

import misc
from misc import debug

class Entity(misc.GameObject):
    def __init__(self, y, x, char):
        super().__init__(y, x) 
        self.char = char
        self.health_points = 0
        self.max_damage = 0
        
    @property
    def hp():
        return self.health_points

    @property
    def damage():
        return random.randint(1, self.max_damage) 
    

class Player(Entity):
    def __init__(self, y, x,):
       super().__init__(y, x, "@")

    def move_relative(self, y_diff, x_diff):
        self.y += y_diff
        self.x += x_diff

    def move(self, y, x):
        self.y = y
        self.x = x

class CorporateZombie(Entity):

    def __init__(self, y, x):
        super().__init__(y, x, "Z")
        self.health_points = random.randint(3, 5)
        self.max_damage = 3
        self.exp_worth = 2

    def decide_move(self, field_of_view):
        player = None
        for obj in field_of_view:
            if isinstance(obj, Player):
                player = obj
                break

        if player:
            debug("Player!", player)
            distance_x = player.x - self.x
            distance_y = player.y - self.y

            delta_x = misc.sign(distance_x)
            delta_y = misc.sign(distance_y)

        else:
            delta_y, delta_x = random.randint(-1, 1), random.randint(-1, 1)

        new_y = self.y + delta_y
        new_x = self.x + delta_x

        return new_y, new_x
