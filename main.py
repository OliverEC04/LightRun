import time
from rpi_ws281x import *
import argparse

# Constants
LEDSIZE = {"x": 5, "y": 60}
BRIGHTNESS = 255 # 0 - 255
MOVESPEED = 5

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

for i in range(5):
    track.append([0])

    for j in range(STRIPCOUNT):
        track[i].append([0])

print(track)

# https://tutorials-raspberrypi.com/how-to-control-a-raspberry-pi-ws2801-rgb-led-strip/