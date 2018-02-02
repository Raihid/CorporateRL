import curses
from misc import debug

class Interface():
    def __init__(self, window):
        self.window = window
        self.height = 24
        self.width = 80
        self.prepare_curses()

        self.shift_y = 1
        self.shift_x = 0

        self.player_message = ""
        self.player_status = ""


    def set_player_status(self, status):
        self.player_status = status

    def prepare_curses(self):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, 11, 0)
        curses.init_pair(2, 22, 0)

    def clear_screen(self):
        for y in range(self.height): 
            for x in range(self.width):
                self.window.addch(y, x, " ")
    
    def draw_tile(self, y, x, obj_):
        assert len(obj_.char) == 1
        color_pair = curses.color_pair(obj_.color)
        self.window.addstr(y + self.shift_y,
                           x + self.shift_x,
                           obj_.char, color_pair)

    def draw_object(self, obj_):
        for y in range(obj_.y, obj_.y  + obj_.h):
            for x in range(obj_.x, obj_.x  + obj_.w):
                self.draw_tile(y, x, obj_)

    def get_user_input(self):
        return self.window.getkey()

    def msg(self, msg):
        self.player_message = msg
    
    
    def display_message(self, y, message):
        for x in range(0, 80):
            self.window.addch(y, x, " ")
        self.window.addstr(y, 0, message)

    def refresh_and_center(self, y, x):
        self.display_message(0, self.player_message)
        self.player_message = ""
        self.display_message(self.height - 1, self.player_status)
        self.window.move(y + self.shift_y, x + self.shift_x)
        self.window.refresh()
