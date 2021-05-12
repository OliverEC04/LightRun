from database import *

# Classes
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Constants
LEDSIZE = Vector2(5, 60)
LEDCOUNT = LEDSIZE.x * LEDSIZE.y
BRIGHTNESS = 255 # 0 - 255
MOVESPEED = 5
DATABASE = Database("../assets/database.db")

#   Pins
LEDPIN = 18
BTNPIN = 6
BTNLEDPIN = 5
BUZZPIN = 16
PRESSRIGHTPIN = 0
PRESSLEFTPIN = 1

# Variables
tick = 0
hitTick = 0
track = []
led = Adafruit_NeoPixel(LEDCOUNT, LEDPIN, 800000, 10, False, BRIGHTNESS, 0)

# Functions
