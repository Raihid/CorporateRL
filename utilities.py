
def GameObject():
    def __init__(pos_x, pos_y, width=1, height=1):
        self.pos_x = pox_x
        self.pos_y = pos_y
        self.width = width
        self.height = height

    @property
    def x(self):
        return self.pos_x

    @property
    def y(self):
        return self.pos_y
        
    @property
    def w(self):
        return self.width

    @property
    def h(self):
        return self.height


def debug_print(msg, level=0)
    if debug_enabled:
        if debug_file:
            debug_file.write(msg + "\n")
        else:
            print(msg)
