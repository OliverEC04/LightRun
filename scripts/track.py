from rpi_ws281x import *
from enum import Enum

class TileType(Enum):
    Empty = 0
    Player = 1
    Wall = 2
    Hole = 3

class Segment:
    def __init__(self):
        pass

    def queue(self):
        pass

class Tile:
    def __init__(self, type):
        self.type = type

    