from rpi_ws281x import *

class Segment:
    def __init__(self):
        pass

    def queue(self):
        pass

class Tile:
    def __init__(self):
        pass

def drawTrack():
    for i in range(LEDCOUNT):
        strip.setPixelColor(i, color)