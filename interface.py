"""Interface support for CorporateRL game."""
import curses
from misc import debug


class Interface():
    """Class representing the curses interface, it's meant to be easily
    replaces with another type of interface.

    Attributes:
        window: curses window in which the game will be displayed.
        shift_y, shift_x (ints): the shift of the game in the window
            so that important interface elements can be displayed.
        player_message (str): message to the player to be displayed in the next
            refresh.
        player_status (str): status of the player (HP and other).
    """

    def __init__(self, window):
        """Initializes the interface in the given window.

        Args:
            window (curses object): a window to display the game.
        """
        self.window = window
        self.height = 24
        self.width = 80
        self.prepare_curses()

        self.shift_y = 1
        self.shift_x = 0

        self.player_message = ""
        self.player_status = ""

    def set_player_status(self, status):
        """Sets the player status.

        Args;
            status (string): player's status to be displayed at the bottom of
                the screen.
        """
        self.player_status = status

    def prepare_curses(self):
        """Set up curses, prepare some colors."""
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, 11, 0)
        curses.init_pair(2, 197, 0)
        curses.init_pair(3, 0, 197)
        curses.init_pair(4, 0, 161)
        curses.init_pair(5, 35, 0)
        curses.init_pair(6, 21, 0)


    def clear_screen(self):
        """Clear the screen, delete all existing characters."""
        for y in range(self.height):
            for x in range(self.width):
                self.window.addch(y, x, " ")

    def draw_tile(self, y, x, obj_):
        """Draw the object at the given position.

        Args:
            y (int): vertical position of the tile
            x (int): horizontal position of the tile
            obj_ (GameObject): object to draw.
        """
        assert len(obj_.char) == 1
        color_pair = curses.color_pair(obj_.color)
        self.window.addstr(y + self.shift_y,
                           x + self.shift_x,
                           obj_.char, color_pair)

    def draw_object(self, obj_):
        """Draw the whole object (possibly multiple tiles).

        Args:
            obj_ (GameObject): object to draw.
        """
        for y in range(obj_.y, obj_.y + obj_.h):
            for x in range(obj_.x, obj_.x + obj_.w):
                self.draw_tile(y, x, obj_)

    def draw_explosion(self, exploded):
        """Draw the explosion with some nice red colors.

        Args:
            exploded (list): list of exploded positions (y, x).
        """
        explosion_color = curses.color_pair(4)
        for (y, x) in exploded:
            self.window.addstr(y + self.shift_y, x + self.shift_x,
                               " ", explosion_color)

    def get_user_input(self):
        """Get the input from the user (keyboard)."""
        key = self.window.getkey()
        debug("Player's input:", key)
        return key

    def msg(self, msg):
        """Set the message to the player.

        Args:
            msg (str): message to set.
        """
        self.player_message = msg

    def display_message(self, y, message):
        """Display the message for the player.

        Args:
            y (int): number of the line on the screen to display in.
            message (str): message to be displayed.
        """
        for x in range(0, 80):
            self.window.addch(y, x, " ")
        self.window.addstr(y, 0, message)

    def refresh_and_center(self, center_y, center_x):
        """Refresh the screen and center the cursos on the given position.

        Args:
            center_y, center_x (ints): position to recenter on.
        """
        self.display_message(0, self.player_message)
        self.player_message = ""
        self.display_message(self.height - 1, self.player_status)
        self.window.move(center_y + self.shift_y, center_x + self.shift_x)
        self.window.refresh()
