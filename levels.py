"""Module implementing level mechanics for CorporateRL game."""
# import interface
import random

import entities
import misc
from misc import debug


GAME_WIDTH = 80
GAME_HEIGHT = 22
SCREEN_HEIGHT = 24


class Wall(misc.GameObject):
    """Class representing a single tile of a wall. May be destroyed.

    Attributes:
        axis (int): integer representing the axis (0 for horizontal, 1 for
            vertical).
    """

    def __init__(self, y, x, h=1, w=1, axis=0):
        super().__init__(y, x, h, w)
        self.visible = True
        self.doors = []
        self.axis = axis
        self.char = "-" if axis == 0 else "|"
        self._color = 1
        self.walkable = False


class Door(misc.GameObject):
    """Class representing a door. Simple as that."""

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
        self.walkable = True

        self.doors = []
        self.char = "."
        # self.items = wylosujmy przedmioty czy cos


class EmptySpace(misc.GameObject):
    def __init__(self, y, x):
        super().__init__(y, x, 1, 1)
        self.visible = True
        self.walkable = True
        self.char = "."


class Stairs(misc.GameObject):
    """Class representing stairs - entrance or exit in the level.

    Attributes:
        axis (int): number representing the way which the stairs leads to: 1
            for downwards and -1 for upwards.
    """

    def __init__(self, y, x, axis):
        assert axis == -1 or axis == 1
        super().__init__(y, x, 1, 1)
        self.walkable = True
        self.char = ">" if axis == 1 else "<"
        self.axis = axis


class Level:
    """Class representing a level and containing a multitude of useful
        functions for running the game and controling the game world.

    Attributes:
        grid (list): A 2D array of dimensions (terminal_height, terminal_width)
            containing references for architecture elements (i.e. rooms, doors,
            walls) at any given point.
        rooms (list): array containing rooms in the level
        visibility (list): A 2D array of dimensions (terminal_height,
            terminal_width) containing boolean values representing whether this
            point on the map is visible or not.
        creatures (list): array containing references to all living creatures
            (player, monsters, bombs) on the map.
        exploded (list): tiles to be drawn as exploded in the next turn.
    """


    def __init__(self, level_num, player, entrance=None):
        self.rooms = []
        self._entrance = entrance if entrance else (15, 15)
        self.grid = [[None for _ in range(GAME_WIDTH)]
                     for _ in range(GAME_HEIGHT)]
        self.visibility = [[False for _ in range(GAME_WIDTH)]
                           for _ in range(GAME_HEIGHT)]

        self.level_num = level_num
        self.player = player
        self.walls = []
        self.doors = []
        self.exploded = []
        self.creatures = [self.player]
        self.generate_level()

    def tick(self):
        """Update situation in the level - set visible rooms etc."""
        top_edge, left_edge, bottom_edge, right_edge = (
            self.get_bounded_range(self.player.y, self.player.x, 1, 1,
                                   additional_radius=1))
        for y in range(top_edge, bottom_edge):
            for x in range(left_edge, right_edge):
                tile = self.grid[y][x]
                if isinstance(tile, Room):
                    self.set_visibility(tile, True, 1)

        if isinstance(tile, Room):
            self.set_visibility(tile, True, 1)

    def in_bounds(self, y, x):
        """Check if the fiven position is in the bound of the level.

        Args:
            y (int): vertical position in the level
            x (int): horizontal position in the level

        Returns:
            True if position is in the level, False otherwise.
        """
        return 0 <= y < GAME_HEIGHT and 0 <= x < GAME_WIDTH

    def recursive_divide(self, y, x, h, w, step=0):
        """Recursively and randomly divide given space.

        This function is used to generate room grid for the given level. The
        next division won't happen if the room is too small or there has been
        to many steps of recursive division or the Random Numbers God says so.

        First, we randomly decide whether to divide the room vertically or
        horizontally. Probabilities for choosing the division axis are set to
        favour square rooms - i.e. the wider the room, the higher the
        probability of choosing vertical division. Then we choose the exact
        point for setting up the wall and pick the door position on said wall.

        For each created room the function is called once again, as "recursive"
        in the name suggests.

        Args:
            y, x, h, w (ints): integers representing in this order: vertical
                position, horizontal position, height and width,
            step (int): number representing the number of steps we've
                completed, useful for stopping condition.
        """
        room_too_small = w < 6 or h < 6
        random_chance = (step > 3 and random.random() < step * 0.04)
        if room_too_small or step > 4 or random_chance:
            return [[y, x, h, w]]

        unnormalized_probs = [h * h * h, w * w * w]
        normalization = sum(unnormalized_probs)
        probs = [prob / normalization for prob in unnormalized_probs]
        axis = misc.random_choice([0, 1], probs=probs)
        doorless = True

        if axis == 0:
            wall_y = random.randint(2, h - 3)
            self.set_wall(y + wall_y, x, 1, w, axis)
            door_x = random.randint(x, x + w)
            divisions = (self.recursive_divide(y, x, wall_y, w, step + 1),
                         self.recursive_divide(y + wall_y + 1, x,
                                               h - (wall_y + 1), w, step + 1))

            while doorless:
                door_x = random.randint(x, x + w - 2)
                first_cond = any((y + wall_y + 1, door_x) in wall
                                 for wall in self.walls)
                second_cond = any((y + wall_y - 1, door_x) in wall
                                  for wall in self.walls)
                doorless = first_cond or second_cond

            self.doors += [Door(y + wall_y, door_x)]
            return divisions[0] + divisions[1]

        elif axis == 1:
            wall_x = random.randint(2, w - 3)
            self.set_wall(y, x + wall_x, h, 1, axis)
            door_y = random.randint(y, y + h)
            divisions = (self.recursive_divide(y, x, h, wall_x, step + 1),
                         self.recursive_divide(y, x + wall_x + 1,
                                               h, w - (wall_x + 1), step + 1))

            while doorless:
                door_y = random.randint(y, y + h - 2)
                first_cond = any((door_y, x + wall_x + 1) in wall
                                 for wall in self.walls)
                second_cond = any((door_y, x + wall_x - 1) in wall
                                  for wall in self.walls)
                doorless = first_cond or second_cond

            self.doors += [Door(door_y, x + wall_x)]
            return divisions[0] + divisions[1]
        else:
            raise ValueError("Axis isn't 0 or 1?!")

    @property
    def architecture(self):
        """Get all "unmovable" objects in the level - rooms, walls, doors and
        stairs in the level.

        Returns:
            Array with references to architecture objects. Order is important.
        """
        return (self.rooms + self.walls + self.doors
                + [self.entrance] + [self.exit])

    def generate_random_monster(self, y, x):
        """Get random monster to put in the level. At the moment only one
        monster available."""
        return entities.CorporateZombie(y, x)

    def generate_stairs(self):
        """Randomly choose a place to place stairs (upwards and downwards).

        Returns:
            Two stairs objects representing entrance and exit.
        """
        entrance_room, exit_room = misc.random_choice(self.rooms, size=2)
        while entrance_room is exit_room:
            exit_room = misc.random_choice(self.rooms)

        entrance_y = random.randrange(entrance_room.y,
                                      entrance_room.y + entrance_room.h)
        entrance_x = random.randrange(entrance_room.x,
                                      entrance_room.x + entrance_room.w)

        entrance = Stairs(entrance_y, entrance_x, -1)

        exit_y = random.randrange(exit_room.y, exit_room.y + exit_room.h)
        exit_x = random.randrange(exit_room.x, exit_room.x + exit_room.w)

        exit_ = Stairs(exit_y, exit_x, 1)
        return entrance, exit_

    def generate_level(self):
        """Generate a new level when the player descends.

        The function divides the level recursively into rooms, places an
        entrance and exit and places some monsters.
        """
        room_coords = self.recursive_divide(0, 0, GAME_HEIGHT, GAME_WIDTH)
        debug(room_coords)

        self.rooms = [Room(y, x, h, w) for y, x, h, w in room_coords]
        self.entrance, self.exit = self.generate_stairs()

        for object_ in self.architecture:
            self.add_to_grid(object_)

        for room in self.rooms:
            threshold = 0.2 + 4 * (room.w * room.h) / (GAME_WIDTH * GAME_HEIGHT)
            while random.random() < threshold:
                tile_y = random.randrange(room.y, room.y + room.h)
                tile_x = random.randrange(room.x, room.x + room.w)
                monster = self.generate_random_monster(tile_y, tile_x)
                self.creatures += [monster]
                threshold = max(0.1, threshold - 0.1)


    def add_to_grid(self, object_):
        """Add the object to the architectural grid of the level.

        Args:
            object_ (GameObject): object to add to the grid.
        """
        for y in range(object_.y, object_.y + object_.h):
            for x in range(object_.x, object_.x + object_.w):
                self.grid[y][x] = object_

    def set_visibility(self, object_, visible, additional_radius=0):
        """Sets the visibility of given object according to the passed values.

        Args:
            object_ (GameObject): object to make visible or invisible.
            visible (boolean): True if we want to make the object visible,
                False if we want to make it invisible.
            additional_radius (int): additional tiles around the object we'd
                like to make visible.
        """
        top_edge, left_edge, bottom_edge, right_edge = (
            self.get_bounded_range(object_.y, object_.x,
                                   object_.h, object_.w,
                                   additional_radius))

        for y in range(top_edge, bottom_edge):
            for x in range(left_edge, right_edge):
                self.visibility[y][x] = visible

    def draw(self, interface):
        """Draw the whole level using the passed interface.

        Args:
            interface (Interface): object representing the game interface.
        """
        interface.clear_screen()

        # Draw all architectural tiles.
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if not self.visibility[y][x] or not cell:
                    continue
                interface.draw_tile(y, x, cell)

        # Draw all visible entities.
        for creature in self.creatures:
            if self.visibility[creature.y][creature.x]:
                interface.draw_object(creature)

        interface.draw_explosion(self.exploded)
        self.exploded = []

    def get_bounded_range(self, y, x, h, w, additional_radius=0):
        """Get range of the arguments taking in account game screen size."""
        top_edge = max(0, y - additional_radius)
        bottom_edge = min(GAME_HEIGHT, y + h + additional_radius)
        left_edge = max(0, x - additional_radius)
        right_edge = min(GAME_WIDTH, x + w + additional_radius)

        return top_edge, left_edge, bottom_edge, right_edge

    def get_tile(self, pos):
        """Get the entity or architectural structure at the given position.

        Args:
            pos (tuple of ints): position of the tile we'd like to get.
        Returns:
            Entity or architectural strucutre at given position.
        """
        y, x = pos
        if not self.in_bounds(y, x):
            return None

        for creature in self.creatures:
            if pos in creature:
                return creature

        return self.grid[y][x]

    def set_wall(self, y, x, h, w, axis):
        """Set a set of one-tile walls on the given area.

        Args;
            y, x, h, w (ints): numbers representing the coordinates where we
                want to set the wall.
            axis (int): wheter the wall is vertical or horizontal.
        """
        for y_ in range(y, y + h):
            for x_ in range(x, x + w):
                self.walls += [Wall(y_, x_, axis=axis)]

    def put_bomb(self, y, x):
        """Puts a bomb at the given position."""
        self.creatures += [entities.Bomb(y, x)]

    def explosion(self, bomb):
        """Calculates results of the explosion of the given bomb.

        Args:
            bomb (Bomb)- a bomb which explodes.
        """
        assert isinstance(bomb, entities.Bomb)

        self.creatures.remove(bomb)
        for creature in self.creatures:
            if not bomb.reaches(creature):
                continue

            # If the second bomb is in range of the first bomb, we'd like
            # to make it explode as well.
            if isinstance(creature, entities.Bomb):
                self.explosion(creature)
            else:
                creature.hp -= 10

        top_edge, left_edge, bottom_edge, right_edge = (
            self.get_bounded_range(bomb.y, bomb.x, 1, 1, bomb.range))

        for y in range(top_edge, bottom_edge):
            for x in range(left_edge, right_edge):
                if bomb.reaches((y, x)):
                    self.exploded += [(y, x)]
                    exploded_obj = self.grid[y][x]
                    if isinstance(exploded_obj, Wall):
                        self.walls.remove(exploded_obj)
                        self.grid[y][x] = EmptySpace(y, x)
                    elif isinstance(exploded_obj, Door):
                        self.doors.remove(exploded_obj)
                        self.grid[y][x] = EmptySpace(y, x)
