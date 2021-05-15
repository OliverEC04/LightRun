import time
import argparse
import sqlite3
import math
from enum import Enum
from rpi_ws281x import *

# Enums
class Tile(Enum):
    Empt = Color(10, 10, 10)
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
    def __init__(self, size, pin, brightness, moveSpeed, tileHeight, seriesConnection = True):
        self.size = size
        self.moveSpeed = moveSpeed
        self.tileHeight = tileHeight
        self.seriesConnection = seriesConnection
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
        for x in range(len(self.track)):
            for y in range(len(self.track[x])):
                if self.tick % self.tileHeight == 0 and y < len(self.track[x]) - 1:
                    self.track[x][y] = self.track[x][y + 1]
                
                # index = self.posToIndex(Vector2(x, y))

                # index = math.floor(self.indexToSeries(self.posToIndex(Vector2(x, y))))
                # print(index)
                # self.led.setPixelColor(index, self.track[x][y].value)
                    
                for i in range(self.tileHeight):
                    trackOffset = self.tick % self.tileHeight
                    # * self.tileHeight + i

                    if self.seriesConnection:
                        stripIndex = math.floor(self.indexToSeries(self.posToIndex(Vector2(x, y))))
                    else:
                        stripIndex = math.floor(self.posToIndex(Vector2(x, y)))

                    print(stripIndex)
                    self.led.setPixelColor(stripIndex, self.track[x][y].value)

        # trackIndex = 0
        # for i in range(self.count - 1):
        #     position = self.indexToPos(i)
        #     trackOffset = self.tick % self.tileHeight

        #     print(position.x, trackIndex + trackOffset)
        #     self.led.setPixelColor(i, self.track[position.x][trackIndex + trackOffset].value)
        #     self.led.show()

        #     if i % self.tileHeight == 0:
        #         trackIndex += 1

        self.led.show()        

        self.tick += 1

    def queueSegment(self, segment):
        for i in range(self.size.x):
            self.track[i].append(Tile.Empt)
            self.track[i].extend(segment.arr[i])
            self.track[i].append(Tile.Empt)

    def posToIndex(self, position):
        return position.x * self.size.y + position.y % self.size.y

    def indexToPos(self, index):
        return Vector2(math.floor(index / self.size.y), index % self.size.y)

    def indexToSeries(self, index):
        if index % (self.size.y * 2) > self.size.y:
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

# Constants
BTNPIN = 6
BTNLEDPIN = 5
BUZZPIN = 16
PRESSRIGHTPIN = 0
PRESSLEFTPIN = 1
STRIP = Strip(Vector2(5, 60), 18, 50, 5, 5, True)
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
STRIP.queueSegment(SEGMENT1)
STRIP.queueSegment(SEGMENT1)

# Loop
while runLoop:
    startTime = time.time()

    STRIP.draw()

    tick += 1
    print("frame tid:", time.time() - startTime)
    time.sleep(max(1 - (time.time() - startTime), 0))





# https://tutorials-raspberrypi.com/how-to-control-a-raspberry-pi-ws2801-rgb-led-strip/