from hx711 import HX711
from rpi_ws281x import *

# Constants
STRIPCOUNT = 30
MOVESPEED = 5

# Pins
STRIPPINS = [7, 8, 2, 3, 4]
BTNPIN = 6
LEDPIN = 5
BUZZPIN = 16
PRESS1PIN = 0
PRESS2PIN = 1

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