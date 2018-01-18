import curses
import time
from utilities import debug_print


class Game:
    def __init__(self):
        self.current_level = Level(number=1)
        self.player = Player()
        # self.interface = Interface()

    def main_loop(stdscr):
        while True:
            world_tick()
            check_world_status()
            user_input = stdscr.getkey()
            stdscr.refresh()

    def draw():
        for item in self.level


directions = {"h": (-1, 0),
              "v": (-1, 1),
              "j": (0, 1),
              "n": (1, 1),
              "l": (1, 0),
              "u": (1, -1),
              "k": (0, -1),
              "y": (-1, -1)}

def main(stdscr):
    # Clear screen
    stdscr.clear()
    win = curses.newwin(24, 80, 0, 0)
    for y in range(0, 23):
        key = stdscr.getkey()
        for x in range(0, 79):
            win.addch(y, x, ord('a') + (x*x+y*y) % 26)

        win.refresh()


    for i in range(0, 10):
        v = i-10

        key = stdscr.getkey()
        stdscr.addstr(i, 0, '10 divided by {} is {}'.format(key, ord(key)))

def generate_level():
    place_rooms()
    make_corridors()
    place_enemies()

def place_rooms():
    rooms_n = random.randint(2, 6)
    rooms_sizes = [random.randint(2, 8, 2) for _ in range(rooms_n)] 

    rooms = []
    for idx, size for enumerate(room_sizes):
        x, y = get_it_randomly_somehow()
        potential_room = Room(x, y, size[0], size[1])
        for existing_room in rooms:
            if self.room_colision(potential_room, existing_room):
                debug_print("Kolizja")
        Room(x, y, w, h)
        
    make_corridors()


if __name__ == "__main__":
    game = Game()
    curses.start_color()
    curses.wrapper(game.main_loop)
