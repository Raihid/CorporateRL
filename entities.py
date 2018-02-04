"""Entity (NPCs, PC, bombs) implementation for CorporateRL game."""
import math
import random

import misc
from misc import debug


class Entity(misc.GameObject):
    """Class representing an abstract entity (PC and NPCs inherit from it).

    Attributes:
        char (str): the ASCII character representing the entity (e.g. @ for
            player character).
        hp (int): the current value of health points.
        max_damage (int): the maximum damage the entity may inflict.
    """

    def __init__(self, y, x, char):
        """Creates an entity, sets its hp and damage.

        Args:
            y (int): vertical position of the character
            x (int): horizontal position of the character
            char (string): the ASCII character representing the entity.
        """
        super().__init__(y, x)
        self.char = char
        self.hp = 0
        self.max_damage = 0

    def damage(self):
        """Get a random number of inflicted damage points."""
        return random.randint(1, self.max_damage)


class Player(Entity):
    """Class representing the player character.

    Attributes:
        max_hp (int): The maximum (initial) number of player health points.
        bombs_n (int): Number of points in player's possesion.
    """
    def __init__(self, y, x):
        """Creates the player, sets its statistics."""
        super().__init__(y, x, "@")
        self.max_hp = 15
        self.max_damage = 3
        self.reset()
        self._color = 6

    def move_relative(self, y_diff, x_diff):
        """Moves the player character relative to its current location.

        Args:
            y_diff (int): vertical distance to move.
            x_diff (int): horizontal distance to move.
        """
        self.y += y_diff
        self.x += x_diff

    def move(self, y, x):
        """Moves the player character to a point on the map.

        Args:
            y (int): target vertical position.
            x (int): target horizontal position.
        """
        self.y = y
        self.x = x

    def reset(self):
        """Resets player's attributes (HP and number of bombs)."""
        self.hp = self.max_hp
        self.bombs_n = 8


class CorporateZombie(Entity):
    """Class representing the most common and the simplest enemy. It's not very
    smart and powerful, but still very dangerous in large groups.

    Attributes:
        exp_worth (int): The amount of experience points the player gets after
            defating the monster. Currently unused.
    """

    def __init__(self, y, x):
        """Creates the zombie, sets up some values."""
        super().__init__(y, x, "Z")
        self.hp = random.randint(3, 5)
        self.max_damage = 2
        self.exp_worth = 2
        self._color = 5

    def make_action(self, field_of_view):
        """Makes a decision where the zombie should move to.

        If the player is in the same room as the zombie, it will walk towards
        him. Otherwise it will just roam around randomly.

        Args:
            field_of_view (list): List of all entities which the NPC sees at
                the given moment.

        Returns:
            Two integers representing the vertical and horizontal position
                after the move.
        """
        player = None
        for obj in field_of_view:
            if isinstance(obj, Player):
                player = obj
                break

        if player:
            distance_x = player.x - self.x
            distance_y = player.y - self.y

            delta_x = misc.sign(distance_x)
            delta_y = misc.sign(distance_y)

        else:
            delta_y, delta_x = random.randint(-1, 1), random.randint(-1, 1)

        new_y = self.y + delta_y
        new_x = self.x + delta_x

        return new_y, new_x


class Bomb(Entity):
    """Class representing a bomb. It's an entity, because it may move around
    and blocks the way for other entities.

    Attributes:
        time_till_blow (int): number of turns until the bomb will explode.
        range (int): all tiles in that distance will be caught in the bomb's
            explosion.
    """

    def __init__(self, y, x):
        """Creates the bomb and sets up default explosion values."""
        super().__init__(y, x, "B")
        self.hp = 1
        self.max_damage = 0
        self.exp_worth = 0
        self.time_till_blow = 6
        self.range = 2

    def damage(self):
        """Returns 0, because bomb doesn't do damage on touch."""
        return 0

    @property
    def color(self):
        """Returns different colors for blinking effect."""
        return 2 + (self.time_till_blow) % 2

    def reaches(self, target):
        """Checks whether the target is in the range of the bomb explosion.

        Args:
            target (tuple or GameObject): the target we want to check for
                range.
        Returns:
            Boolean value representing where the target is in range.
        """
        if isinstance(target, misc.GameObject):
            y = target.y
            x = target.x
        elif isinstance(target, tuple) and len(target) == 2:
            y, x = target
        else:
            raise ValueError("Not a position and not a creature!")

        delta_y = self.y - y
        delta_x = self.x - x

        distance = math.sqrt(delta_y * delta_y + delta_x * delta_x)
        debug("Dystans", distance, self.range)
        return distance <= self.range

    def make_action(self, field_of_view):
        """Makes the bomb fuse shorter.

        Returns:
            Two integers representing bomb's vertical and horizontal position.
        """
        self.time_till_blow -= 1
        return self.y, self.x
