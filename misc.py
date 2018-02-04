"""Various helper functions for CorporateRL game."""
import datetime
import random

DEBUG_ENABLED = True
DEBUG_FILE = open("corporate.log", "a")


class GameObject():
    """Generic class representing a game object which has 2D position, width
    and height.

    Attributes:
        y (int):
        x (int):
        w (int): width of the object.
        h (int): height of the object.
        _color (int): represents the curses color_pair of the object.
        walkable (boolean): whether the entities in the world can walk on this
        object.
    """
    def __init__(self, pos_y, pos_x, height=1, width=1):
        """Creates the object with some generic attributes.

        Args:
            pos_y (int): vertical position of the object.
            pos_x (int): horizontal position of the object.
            height (int): height of the object.
            width (int): width of the object.
        """
        self.pos_y = pos_y
        self.pos_x = pos_x
        self.height = height
        self.width = width
        self.x = pos_x
        self.y = pos_y
        self.w = width
        self.h = height
        self._color = 0
        self.walkable = False

    def __contains__(self, pos):
        """Check whether the given position ois "inside" the object.

        Args:
           pos (obj or tuple of ints): represent the object or position of the
               object we want to check.
        Returns:
            True if the position is inside the object, False otherwise.
        """
        if isinstance(pos, GameObject):
            pos = (pos.y, pos.x)
        if not isinstance(pos, tuple) or len(pos) != 2:
            raise ValueError("This is not a position!")
        return (pos[0] >= self.y and pos[0] < self.y + self.h and
                pos[1] >= self.x and pos[1] < self.x + self.w)

    @property
    def color(self):
        """Getter for color."""
        return self._color


def random_choice(container, size=None, probs=None):
    """Helper function to implement random.choice with probabilities and
    ability to choose element multiple times.

    Args:
        container (iterable): the container we'd like to choose from.
        size (int): how many element's we'd like to choose.
        probs (list of ints): probabilities of elements

    Returns:
        Chosen element if size is None, otherwise list of chosen elements of
        length size.
    """
    def get_element(container, probs):
        """Gets the element with given container and probs.

        Args:
            container (iterable): the container we'd like to choose from.
            probs (list of ints): probabilities of elements
        Returns:
            One element from the container.
        """
        roll = random.random()
        debug("Roll:", roll)
        probs_sum = 0
        for idx, prob in enumerate(probs):
            probs_sum += prob
            if roll <= probs_sum:
                return container[idx]
        raise ValueError("Probs don't sum to one?!")

    len_ = len(container)
    if probs is None:
        probs = [1 / len_ for _ in range(len_)]

    if size is None:
        return get_element(container, probs)
    return [get_element(container, probs) for _ in range(size)]


def sign(x):
    """Helper function implementing the np.sign functionality.

    Args:
        x (Number): number to be given sign of.

    Returns:
        Sign of the x as integer.
    """
    if x == 0:
        return 0
    return 1 if x > 0 else -1


def debug(*args):
    """Helper function for printing to the log file."""
    strargs = [str(arg) for arg in args]
    msg = "\t".join(strargs)
    if DEBUG_ENABLED:
        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = time_now + "\t" + msg
        if DEBUG_FILE:
            DEBUG_FILE.write(msg + "\n")
            DEBUG_FILE.flush()
        else:
            print(msg)
