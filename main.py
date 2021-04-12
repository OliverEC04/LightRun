# Pins
STRIPPINS = [7, 8, 2, 3, 4]
BTNPIN = 6
LEDPIN = 5
BUZZPIN = 16
PRESS1PIN = 0
PRESS2PIN = 1

# Constants
STRIPCOUNT = 30
MOVESPEED = 5

# Variables
tick = 0
hitTick = 0
track = []

print("hej")

for i in range(5):
    for j in range(STRIPCOUNT):
        track[i][j] = 0

print(track)