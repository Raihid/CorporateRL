# import interface
import misc
import numpy as np
import random
from misc import debug


GAME_WIDTH = 80
GAME_HEIGHT = 22
SCREEN_HEIGHT = 24



class Wall(misc.GameObject):
    def __init__(self, y, x, h, w, axis):
        super().__init__(y, x, h, w)
        self.visible = True
        self.doors = []
        self.axis = axis
        self.char = "-" if axis == 0 else "|"
        self.color = 1
        self.walkable = False


class Door(misc.GameObject):
    def __init__(self, y, x):
        super().__init__(y, x)
        self.visible = True
        self.doors = []
        self.char = "+"
        self.walkable = True


class Room(misc.GameObject):

    def __init__(self, y, x, h, w):
        super().__init__(y, x, h, w)
        self.visible = False

        self.doors = []
        self.char = "."
        # self.items = wylosujmy przedmioty czy cos

    def is_door(self, pos):
        return False

    def is_interior(self, pos):
        return True


class Level:
    def __init__(self, level_num, player, entrance=None):
        self.rooms = []
        self._entrance = entrance if entrance else (15, 15)
        self.grid = [[list() for _ in range(GAME_WIDTH)]
                        for _ in range(GAME_HEIGHT)]
        self.visibility = [[False for _ in range(GAME_WIDTH)]
                                for _ in range(GAME_HEIGHT)]

        self.level_num = level_num
        self.player = player
        self.walls = []
        self.doors = []
        self.generate_level()

    def tick(self):
        for room in self.rooms:
            pos = (self.player.y, self.player.x)
            if pos in room:
                room.visible = True

    def recursive_divide(self, y, x, h, w, step=0):
        if (w < 6 or h < 6 or step > 4 or (step > 3 and random.random() < step * 0.04)):
            return [[y, x, h, w]]

        normalization = w * w + h * h
        axis = np.random.choice([0, 1], p=[h * h / normalization, w * w / normalization])
        doorless = True

        if axis == 0:
            wall_y = random.randint(2, h - 3)
            self.walls += [Wall(y + wall_y, x, 1, w, axis)]
            door_x = random.randint(x, x + w)
            divisions = (self.recursive_divide(y, x, wall_y, w, step + 1),
                         self.recursive_divide(y + wall_y + 1, x,
                                               h - (wall_y + 1), w, step + 1))

            while doorless:
                door_x = random.randint(x, x + w - 2)
                first_cond = any((y + wall_y + 1, door_x) in wall for wall in self.walls)
                second_cond = any((y + wall_y - 1, door_x) in wall for wall in self.walls)
                doorless = first_cond or second_cond

            self.doors += [Door(y + wall_y, door_x)]
            return divisions[0] + divisions[1]

        elif axis == 1:
            wall_x = random.randint(2, w - 3)
            self.walls += [Wall(y, x + wall_x, h, 1, axis)]
            door_y = random.randint(y, y + h)
            divisions = (self.recursive_divide(y, x, h, wall_x, step + 1),
                        self.recursive_divide(y, x + wall_x + 1,
                                          h, w - (wall_x + 1), step + 1))

            while doorless:
                door_y = random.randint(y, y + h - 2)
                first_cond = any((door_y, x + wall_x + 1) in wall for wall in self.walls)
                second_cond = any((door_y, x + wall_x - 1) in wall for wall in self.walls)
                doorless = first_cond or second_cond

            self.doors += [Door(door_y, x + wall_x)]
            return divisions[0] + divisions[1]

    @property
    def architecture(self):
        return self.rooms + self.walls + self.doors

    @property
    def items(self):
        return []

    @property
    def entities(self):
        return [self.player]


    def generate_level(self):
        room_coords = self.recursive_divide(0, 0, GAME_HEIGHT, GAME_WIDTH)
        debug(room_coords)

        self.rooms = [Room(y, x, h, w) for y, x, h, w in room_coords]
        
        for object_ in self.architecture:
            self.add_to_grid(object_)
    
    def add_to_grid(self, object_):
        for y in range(object_.y, object_.y + object_.h):
            for x in range(object_.x, object_.x + object_.w):
                self.grid[y][x] += [object_]
            
    def set_visibility(self, object_, visible, additional_radius=0):
        left_edge = max(0, object_.x - additional_radius)
        right_edge = min(GAME_WIDTH, object_.x + object_.w + additional_radius)
        top_edge = max(0, object_.y - additional_radius)
        bottom_edge = min(GAME_HEIGHT, object_.y + object_.h + additional_radius)
         
        for y in range(top_edge, bottom_edge):
            for x in range(left_edge, right_edge):
                self.visibility[y][x] = visible

    @property
    def entrance(self):
        return self._entrance

    def draw(self, interface):
        debug(self.grid)
        interface.clear_screen() 

        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if not self.visibility[y][x] or not cell:
                # if not cell:
                    continue
                topmost = cell[-1]
                interface.draw_tile(y, x, topmost)
                debug(y, x, topmost)

        for item in self.items:
            interface.draw_object(entity)

        for entity in self.entities:
            interface.draw_object(entity)


    def get_tile_type(self, pos):
        for room in self.rooms:
            if (pos[0] >= room.y and pos[0] < room.y + room.h and
                    pos[1] >= room.x and pos[1] < room.x + room.w):

                self.set_visibility(room, True, additional_radius=1)

                return "WALKABLE"
        for door in self.doors:
            if pos[0] == door.y and pos[1] == door.x:
                return "WALKABLE"

        return "WALL"
