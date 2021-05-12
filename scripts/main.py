import time
import argparse
import sqlite3
import math
from enum import Enum
from rpi_ws281x import *

# Enums
class TileType(Enum):
    Empty = Color(0, 0, 0)
    Player = Color(0, 255, 0)
    Wall = Color(255, 0, 0)
    Hole = Color(0, 0, 255)

# Classes
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Segment:
    def __init__(self):
        pass

    def queue(self):
        pass

class Tile:
    def __init__(self, type):
        self.type = type

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
STRIP = Strip(Vector2(5, 60), 18, 20, 5)
DATABASE = Database("../assets/database.db")

# Variables
tick = 0
hitTick = 0

# Intialize
STRIP.draw()







# https://tutorials-raspberrypi.com/how-to-control-a-raspberry-pi-ws2801-rgb-led-strip/