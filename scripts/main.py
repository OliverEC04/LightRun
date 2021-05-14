import time
import argparse
import sqlite3
import math
from enum import Enum
from rpi_ws281x import *

# Enums
class Tile(Enum):
    Empt = Color(1, 1, 1)
    User = Color(0, 255, 0)
    Wall = Color(255, 0, 0)
    Hole = Color(0, 0, 255)

# Classes
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Segment:
    def __init__(self, segmentArray):
        self.arr = segmentArray

class Strip:
    def __init__(self, size, pin, brightness, moveSpeed, tileHeight):
        self.size = size
        self.moveSpeed = moveSpeed
        self.tileHeight = tileHeight
        self.tick = 0
        self.track = []
        self.count = size.x * size.y
        self.led = Adafruit_NeoPixel(self.count, pin, 800000, 10, False, brightness, 0)

        for x in range(self.size.x):
            self.track.append([])

            for y in range(math.ceil(self.size.y / self.tileHeight)):
                self.track[x].append(Tile.Empt)

        self.track[math.floor(self.size.x / 2)][1] = Tile.User

        self.led.begin()

    def draw(self):
        # Move track down
        # if (self.tick % self.tileHeight == 0):
        #     for x in range(len(self.track) - 1):
        #         for y in range(len(self.track[x]) - 1):
        #             self.track[x][y] = self.track[x][y + 1]

        # Draw to strips
        # for x in range(len(self.track)):
        #     for y in range(len(self.track[x])):
        #         if self.tick % self.tileHeight == 0 and y < len(self.track[x]) - 1:
        #             self.track[x][y] = self.track[x][y + 1]

        #         for i in range(self.tileHeight):
        #             stripIndex = self.posToIndex(Vector2(x, y)) + i
        #             self.led.setPixelColor(stripIndex, self.track[x][y].value)
        #             self.led.show()

        for i in range(self.count):
            self.led.setPixelColor(i, Color(40, 100, 240))
            self.led.show()

        # trackIndex = 0
        # for i in range(self.count - 1):
        #     position = self.indexToPos(i)
        #     trackOffset = self.tick % self.tileHeight

        #     print(position.x, trackIndex + trackOffset)
        #     self.led.setPixelColor(i, self.track[position.x][trackIndex + trackOffset].value)
        #     self.led.show()

        #     if i % self.tileHeight == 0:
        #         trackIndex += 1

        self.tick += 1

    def queueSegment(self, segment):
        for i in range(self.size.x):
            self.track[i].extend(segment.arr[i])

    def posToIndex(self, position):
        return position.x * self.size.y + position.y % self.size.y

    def indexToPos(self, index):
        return Vector2(math.floor(index / self.size.y), index % self.size.y)

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

# Constants
BTNPIN = 6
BTNLEDPIN = 5
BUZZPIN = 16
PRESSRIGHTPIN = 0
PRESSLEFTPIN = 1
STRIP = Strip(Vector2(5, 60), 18, 50, 5, 5)
DATABASE = Database("../assets/database.db")
SEGMENT1 = Segment([
    [Tile.Wall, Tile.Wall, Tile.Empt, Tile.Hole],
    [Tile.Empt, Tile.Empt, Tile.Empt, Tile.Hole],
    [Tile.Wall, Tile.Wall, Tile.Empt, Tile.Empt],
    [Tile.Empt, Tile.Hole, Tile.Empt, Tile.Wall],
    [Tile.Wall, Tile.Empt, Tile.Empt, Tile.Wall]
])

# Variables
tick = 0
hitTick = 0
runLoop = True

# Intialize
STRIP.queueSegment(SEGMENT1)

# Loop
while runLoop:
    startTime = time.time()

    STRIP.draw()

    tick += 1
    print(time.time() - startTime)
    #time.sleep(max(1 - (time.time() - startTime), 0))





# https://tutorials-raspberrypi.com/how-to-control-a-raspberry-pi-ws2801-rgb-led-strip/