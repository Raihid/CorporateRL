import curses
import levels
import time
import misc
from misc import debug_print


directions = {"h": (0, -1),
              "v": (1, -1),
              "j": (1, 0),
              "n": (1, 1),
              "l": (0, 1),
              "u": (-1, 1),
              "k": (-1, 0),
              "y": (-1, -1)}

# Wymyslic mape 
# Niech interfejs rysuje wszystko 
class Game:
    def __init__(self):
        self.current_level = levels.Level(level_num=1)
        self.player = Player(0, 0)
        self.window = None

    def main_loop(self, stdscr):
        self.window = stdscr
        curses.start_color()
        self.current_level.draw(self.window)
        self.player.move(*self.current_level.entrance)
        self.window.addch(*self.current_level.entrance, "@")

        while True:
            self.world_tick()
            self.check_world_status()
            user_input = stdscr.getkey()
            self.interpret_input(user_input)
            stdscr.refresh()
            self.window.move(self.player.y, self.player.x)

    def player_message(self, msg):
        for x in range(0, 24):
            self.window.delch(0, x)
        self.window.addstr(0, 0, msg)

    def interpret_input(self, user_input):
        if user_input in directions.keys():
            direction = directions[user_input]
            new_pos = (self.player.y + direction[0],
                       self.player.x + direction[1]) 
            tile_type = self.current_level.get_tile_type(new_pos)

            if tile_type == "WALL":
                # debug_print("Player has walken into the wall, ignorning")
                pass
            elif tile_type == "WALKABLE":
                self.player_message("We're walking!")
                self.window.addch(self.player.y, self.player.x, ".")
                self.player.move_relative(*direction)
                self.window.addch(*new_pos, "@")

            elif tile_type == "MONSTER":
                raise NotImplementedError("Fight hasn't been implemented yet :(")

            else:
                raise NotImplementedError("What")

        else:
            self.player_message("I don't understand what you want me to do")

    def check_world_status(self):
        pass

    def world_tick(self):
        pass


class Player(misc.GameObject):
    def __init__(self, y, x):
       super().__init__(y, x) 

    def move_relative(self, y_diff, x_diff):
        self.y += y_diff
        self.x += x_diff

    def move(self, y, x):
        self.y = y
        self.x = x


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
    for idx, size in enumerate(room_sizes):
        x, y = get_it_randomly_somehow()
        potential_room = Room(x, y, size[0], size[1])
        for existing_room in rooms:
            if self.room_colision(potential_room, existing_room):
                debug_print("Kolizja")
        Room(x, y, w, h)
        
    make_corridors()


if __name__ == "__main__":
    game = Game()
    curses.wrapper(game.main_loop)
