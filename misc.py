import datetime

DEBUG_ENABLED = True
DEBUG_FILE = open("corporate.log", "a")

class GameObject():
    def __init__(self, pos_y, pos_x, height=1, width=1):
        self.pos_y = pos_y
        self.pos_x = pos_x
        self.height = height
        self.width = width
        self.x = pos_x
        self.y = pos_y
        self.w = width
        self.h = height
        self.color = 0
        self.walkable = False

    def __contains__(self, pos):
        if isinstance(pos, GameObject):
            pos = (pos.y, pos.x)
        if not isinstance(pos, tuple) or len(pos) != 2:
            raise ValueError("This is not a position!")
        return (pos[0] >= self.y and pos[0] < self.y + self.h and
                pos[1] >= self.x and pos[1] < self.x + self.w)

    # @property
    # def x(self):
    #     return self.pos_x

    # @property
    # def y(self):
    #     return self.pos_y
    #     
    # @property
    # def w(self):
    #     return self.width

    # @property
    # def h(self):
    #     return self.height

def sign(x):
    if x == 0:
        return 0
    else:
        return (1 if x > 0 else -1)

def debug(*args, level=0):
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
