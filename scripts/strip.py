from scripts.globalVar import Vector2
from rpi_ws281x import *
from globalVar import *

class Strip:
    def __init__(self, size, pin, brightness):
        self.size = size
        self.count = size.x * size.y
        self.led = Adafruit_NeoPixel(self.count, pin, 800000, 10, False, brightness, 0)

    def draw(self):
        for i in range(self.count):
            self.led.setPixelColor(i, color)

    def posToIndex(self, position):
        return position.x * self.size.y + position.y % self.size.y

    def indexToPos(self, index):
        return Vector2()
            