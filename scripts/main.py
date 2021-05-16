import time
import argparse
import sqlite3
import math
import RPi.GPIO as GPIO
from enum import Enum
from rpi_ws281x import *

"""
TODO:
 * Movement
   * Spiller
   * Fodplader
   * Knapper
   * Dø
   * Hop
 * Pointgivning og scoreboard
   * Optæl point når man spiller
   * Skriv pointene til database
   * Vis scoreboard på LCD
 * Transition på LEDer måske
"""

# Enums
class Tile(Enum):
    Empt = Color(10, 10, 10)
    User = Color(0, 255, 0)
    Wall = Color(255, 0, 0)
    Hole = Color(0, 0, 255)

# Constants
LOOPSPEED = .1 # How long each loop takes (seconds)

# Declaring variables
tick = 0
hitTick = 0
runLoop = 0
startGame = 0
strip = 0
database = 0
segments = 0
pressLed = 0
buzz = 0
btn = 0
pressRight = 0
pressLeft = 0

# Classes
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class BinIn:
    def __init__(self, pin):
        self.pin = pin

        GPIO.setup(self.pin, GPIO.IN)
    
    def pressed(self):
        return GPIO.input(self.pin) == 1

class BinOut:
    def __init__(self, pin):
        self.pin = pin

        GPIO.setup(self.pin, GPIO.OUT)

    def write(self, output):
        GPIO.output(self.pin, output)

class Segment:
    def __init__(self, segmentArray):
        self.arr = segmentArray

class User:
    def __init__(self, strip):
        self.position = 0
        self.jump = False
        self.strip = strip
    
    def moveRight(self):
        if self.position > 0:
            self.position -= 1

    def moveLeft(self):
        if self.position < self.strip.size.x - 1:
            self.position += 1

    def collide(self):
        resetGame()

class Strip:
    def __init__(self, size, pin, brightness, moveSpeed, tileHeight, seriesConnection = True):
        self.size = size
        self.moveSpeed = moveSpeed
        self.tileHeight = tileHeight
        self.seriesConnection = seriesConnection
        self.tick = 0
        self.track = []
        self.count = size.x * size.y
        self.led = Adafruit_NeoPixel(self.count, pin, 800000, 10, False, brightness, 0)

        self.initializeTrack()
        self.led.begin()

    def draw(self):
        self.tick += 1

        # Limit to moveSpeed
        if self.tick % self.moveSpeed != 0:
            return

        # Move track down
        if (self.tick % self.tileHeight == 0):
            for x in range(len(self.track)):
                for y in range(len(self.track[x]) - 1):
                    self.track[x][y] = self.track[x][y + 1]

        # Draw track to strips
        for x in range(self.size.x):
            for y in range(self.size.y):
                if y < self.tileHeight:
                    trackOffset = 0
                else:
                    trackOffset = self.tick % self.tileHeight

                posIndex = self.posToIndex(Vector2(x, y)) - trackOffset

                if self.seriesConnection:
                    stripIndex = math.floor(self.indexToSeries(posIndex))
                else:
                    stripIndex = math.floor(posIndex)

                self.led.setPixelColor(stripIndex, self.track[x][math.floor(y / self.tileHeight)].value)

        # Draw user
        self.led.setPixelColor(self.posToIndex(Vector2(self.user.position, self.tileHeight)), Tile.User.value)

        self.led.show()

        # Collision detection
        if self.track[self.user.position][1] != Tile.Empt:
            self.user.collide()

    def queueSegment(self, segment):
        for i in range(self.size.x):
            self.track[i].append(Tile.Empt)
            self.track[i].extend(segment.arr[i])
            self.track[i].append(Tile.Empt)

    def addUser(self, user):
        self.user = user
        self.user.position = math.floor(self.size.x / 2)

    def reset(self):
        self.initializeTrack()

    def initializeTrack(self):
        self.track = []

        for x in range(self.size.x):
            self.track.append([])

            for y in range(math.ceil(self.size.y / self.tileHeight)):
                self.track[x].append(Tile.Empt)

    def posToIndex(self, position):
        return position.x * self.size.y + position.y % self.size.y

    def indexToPos(self, index):
        return Vector2(math.floor(index / self.size.y), index % self.size.y)

    def indexToSeries(self, index):
        if index % (self.size.y * 2) >= self.size.y:
            midIndex = self.size.y * (self.indexToPos(index).x + 1) - self.size.y / 2
            return (midIndex - index) * 2 + index - 1
        else:
            return index

class Database:
    def __init__(self, path):
        self.path = path

    def insertScore(self, user, score):
        status = "waiting"
        date = 1

        try:
            sqliteConnection = sqlite3.connect(self.path)
            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")

            sqlite_insert_query = """INSERT INTO Scoreboard
                                (name, score, date) 
                                VALUES 
                                ('{0}','{1}','{2}')""".format(user, score, date)

            count = cursor.execute(sqlite_insert_query)
            sqliteConnection.commit()
            print("Record inserted successfully into Scoreboard table", cursor.rowcount)
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("The SQLite connection is closed")

# Functions
def initialize():
    global runLoop
    global strip
    global database
    global pressLed
    global btn
    global pressRight
    global pressLeft
    global segments

    runLoop = True
    strip = Strip(Vector2(5, 60), 18, 50, 1, 5, True)
    database = Database("../assets/database.db")
    segments = [
        Segment([
            [Tile.Wall, Tile.Wall, Tile.Empt, Tile.Hole],
            [Tile.Empt, Tile.Empt, Tile.Empt, Tile.Hole],
            [Tile.Wall, Tile.Wall, Tile.Empt, Tile.Empt],
            [Tile.Empt, Tile.Hole, Tile.Empt, Tile.Wall],
            [Tile.Wall, Tile.Empt, Tile.Empt, Tile.Wall]
        ]),
    ]

    strip.queueSegment(segments[0])
    # STRIP.queueSegment(SEGMENT1)
    # STRIP.queueSegment(SEGMENT1)
    strip.addUser(User(strip))

    GPIO.setmode(GPIO.BOARD)

    pressLed = BinOut(29)
    btn = BinIn(31)
    pressRight = BinIn(35)
    pressLeft = BinIn(33)

def resetGame():
    global startGame

    startGame = False

    strip.reset()
    initialize()
    strip.draw()

# Variables
tick = 0
hitTick = 0


# Temp
startGame = True


print("Tryk CTRL + C for at stoppe programmet")
initialize()

# Loop
while runLoop:
    startTime = time.time()

    if startGame:
        strip.draw()
    else:
        startGame = btn.pressed()
        if startGame:
            pressLed.write(False)
        else:
            pressLed.write(tick % 2)

    tick += 1
    print("frame tid:", time.time() - startTime)
    time.sleep(max(LOOPSPEED - (time.time() - startTime), 0))





# https://tutorials-raspberrypi.com/how-to-control-a-raspberry-pi-ws2801-rgb-led-strip/