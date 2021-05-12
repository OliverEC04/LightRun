from strip import *
from database import *

# Classes
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Constants
BTNPIN = 6
BTNLEDPIN = 5
BUZZPIN = 16
PRESSRIGHTPIN = 0
PRESSLEFTPIN = 1
STRIP = Strip(Vector2(5, 60), 18, 20, 5)
DATABASE = Database("../assets/database.db")

# Variables
tick = 0
hitTick = 0

# Functions
