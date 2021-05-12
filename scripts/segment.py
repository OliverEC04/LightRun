from rpi_ws281x import *
from enum import Enum
from globalVar import *

class TileType(Enum):
    Empty = Color(0, 0, 0)
    Player = Color(0, 255, 0)
    Wall = Color(255, 0, 0)
    Hole = Color(0, 0, 255)

class Segment:
    def __init__(self):
        pass

    def queue(self):
        pass

class Tile:
    def __init__(self, type):
        self.type = type

    