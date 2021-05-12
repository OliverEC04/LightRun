import time
from rpi_ws281x import *
import argparse
from globalVar import *
from database import *
from track import *

# Intialize
for i in range(LEDSIZE.x):
    track.append([])

    for j in range(LEDSIZE.y):
        track[i].append([Tile()])

print(track)

# https://tutorials-raspberrypi.com/how-to-control-a-raspberry-pi-ws2801-rgb-led-strip/