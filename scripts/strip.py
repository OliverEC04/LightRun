import math
from rpi_ws281x import *
from globalVar import *
from segment import *
from database import *

class Strip:
    def __init__(self, size, pin, brightness, moveSpeed):
        self.size = size
        self.moveSpeed = moveSpeed
        self.count = size.x * size.y
        self.track = []
        self.led = Adafruit_NeoPixel(self.count, pin, 800000, 10, False, brightness, 0)

        for x in range(self.size.x):
            self.track.append([])

            for y in range(self.size.y):
                self.track[x].append(Tile(TileType.Empty))

        self.track[math.floor(self.size.x / 2)][1] = TileType.Player

    def draw(self):
        for i in range(self.count):
            position = self.indexToPos(i)
            self.led.setPixelColor(i, self.track[position.x][position.y].type)

    def posToIndex(self, position):
        return position.x * self.size.y + position.y % self.size.y

    def indexToPos(self, index):
        return Vector2(math.floor(index / self.size.y), index % self.size.y)
            