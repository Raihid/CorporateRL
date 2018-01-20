import misc


class Level:
    def __init__(self, level_num):
        self.rooms = [Room(10, 10, 10, 10)]
        self._entrance = (15, 15)
    
    @property
    def entrance(self):
        return self._entrance
        
    def draw(self, window):
        window.clear()
        for room in self.rooms:
            room.draw(window)

    def get_tile_type(self, pos):
        for room in self.rooms:
            if (pos[0] >= room.y and pos[0] < room.y + room.h and
                    pos[1] >= room.x and pos[1] < room.x + room.w):

                if room.is_door(pos) or room.is_interior(pos):
                    return "WALKABLE"

                else:
                    return "WALL"
        
        

class Room(misc.GameObject):
    
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.visible = True
        self.doors = None
        # self.items = wylosujmy przedmioty czy cos

    def is_door(self, pos):
        return False

    def is_interior(self, pos):
        return (pos[0] >= self.y + 1 and pos[0] < self.y + self.h - 1 and
                pos[1] >= self.x + 1 and pos[1] < self.x + self.w - 1)

    def draw(self, window):
        # Draw horizontal walls
        for y in [self.y, self.y + self.h - 1]:
            for x in range(self.x, self.x + self.w):
                window.addch(y, x, "-")

        # Draw vertical walls
        for x in [self.x, self.x + self.w - 1]: 
            for y in range(self.y + 1, self.y + self.h - 1):
                window.addch(y, x, "|")

        # Draw interor of the room
        for y in range(self.y + 1, self.y + self.h - 1):
            for x in range(self.x + 1, self.x + self.w - 1):
                window.addch(y, x, ".")
