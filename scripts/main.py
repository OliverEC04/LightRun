import time
import argparse
import sqlite3
import math
# import I2C_LCD_driver
import psgui as sg
from enum import Enum
try:
    import RPi.GPIO as GPIO
    from rpi_ws281x import *
except:
    CROSSPLATFORM = True

"""
TODO:
 * Movement
   * Spiller ✔
   * Fodplader
   * Knapper ✔
   * Dø ✔
   * Hop (nej)
 * Pointgivning og scoreboard
   * Optæl point når man spiller
   * Skriv pointene til database
   * Vis scoreboard på LCD
 * Transition på LEDer måske
"""

# Enums
class Tile(Enum):
    Empt = Color(0, 0, 0)
    User = Color(0, 255, 0)
    Wall = Color(200, 0, 0)
    Hole = Color(200, 0, 0)

# Constants
LOOPSPEED = .1 # How long each loop takes (seconds)
ENABLENAME = False

# Declaring variables
tick = 0
hitTick = 0
runLoop = 0
startGame = 0
strip = 0
database = 0
segments = 0
window = 0
layoutIn = 0
layoutOut = 0
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
        self.strip = strip
        self.position = Vector2(math.floor(self.strip.size.x / 2), self.strip.tileHeight)
        self.jump = False
        self.btnControls = True
    
    def update(self):
        # Movement
        if self.btnControls:
            try:
                if self.rightBtn.pressed():
                    self.moveRight()
            except:
                print("User has no right control!")
            
            try:
                if self.leftBtn.pressed():
                    self.moveLeft()
            except:
                print("User has no left control!")

        # Draw to strip
        if startGame:
            self.strip.draw(self.position, Tile.User)
        else:
            for x in range(self.strip.size.x):
                if x == self.position.x:
                    self.strip.draw(self.position, Tile.User)
                else:
                    self.strip.draw(Vector2(x, self.position.y), Tile.Empt)

        self.strip.led.show()

        # Collision detection
        if self.strip.track[self.position.x][1] != Tile.Empt:
            self.collide()

    def bindControls(self, rightBtn = 0, leftBtn = 0):
        if rightBtn != 0:
            self.rightBtn = rightBtn

        if leftBtn != 0:
            self.leftBtn = leftBtn

    def moveRight(self):
        if self.position.x > 0:
            self.position.x -= 1

    def moveLeft(self):
        if self.position.x < self.strip.size.x - 1:
            self.position.x += 1

    def setPosition(self, value):
        self.position.x = round(value / 100 * self.strip.size.x)

    def collide(self):
        buzz.write(True)
        time.sleep(0.5)
        buzz.write(False)

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

        self.led.begin()
        self.initializeTrack()

    def update(self):
        self.tick += 1

        # Loop track
        try:
            if (self.tick / (self.moveSpeed / self.tileHeight)) % self.segmentsEnd == 0:
                self.queueSegment(Segment(self.segmentsCombined))

        except:
            print("No segment loop")

        # Move track down
        if self.tick % self.tileHeight == 0 and self.tick % self.moveSpeed == 0:
            for x in range(len(self.track)):
                for y in range(len(self.track[x]) - 1):
                    self.track[x][y] = self.track[x][y + 1]

        # Draw track to strips
        for x in range(self.size.x):
            for y in range(self.size.y):
                if y < self.tileHeight:
                    trackOffset = 0
                else:
                    trackOffset = math.floor(self.tick / (self.moveSpeed / self.tileHeight)) % self.tileHeight

                self.draw(Vector2(x, y - trackOffset), self.track[x][math.floor(y / self.tileHeight)])

        self.led.show()        

    def queueSegment(self, segment):
        for i in range(self.size.x):
            self.track[i].append(Tile.Empt)
            self.track[i].extend(segment.arr[i])

    def loopSegments(self, segments):
        self.segmentsCombined = []

        for x in range(self.size.x):
            self.segmentsCombined.append([])
            
            for i in range(len(segments)):
                self.segmentsCombined[x].extend(segments[i].arr[x])
        
        self.queueSegment(Segment(self.segmentsCombined))

        self.segmentsEnd = len(self.segmentsCombined[0])

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
                
                for i in range(self.tileHeight):
                    self.led.setPixelColor(self.posToIndex(Vector2(x, y * self.tileHeight + i)), Tile.Empt.value)

        self.led.show()

    def draw(self, position, tile):
        if self.seriesConnection:
            index = math.floor(self.indexToSeries(self.posToIndex(position)))
        else:
            index = math.floor(self.posToIndex(position))

        self.led.setPixelColor(index, tile.value)

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
def resetGame():
    global startGame

    startGame = False

    strip.reset()
    strip.queueSegment(segments[0])

# Temp
startGame = True

# Initalize
print("Tryk CTRL + C for at stoppe programmet")
GPIO.setmode(GPIO.BOARD)

tick = 0
hitTick = 0
runLoop = True
pressLed = BinOut(29)
buzz = BinOut(38)
btn = BinIn(31)
pressRight = BinIn(35)
pressLeft = BinIn(33)
database = Database("../assets/database.db")
strip = Strip(Vector2(5, 60), 18, 50, 10, 5, True)
user = User(strip)
segments = [
    Segment([
        [Tile.Wall, Tile.Wall, Tile.Empt, Tile.Hole],
        [Tile.Empt, Tile.Empt, Tile.Empt, Tile.Hole],
        [Tile.Wall, Tile.Wall, Tile.Empt, Tile.Empt],
        [Tile.Empt, Tile.Hole, Tile.Empt, Tile.Wall],
        [Tile.Wall, Tile.Empt, Tile.Empt, Tile.Wall]
    ]),
]

inCol = [
    [sg.Text("Du er logget in som")],
    [sg.Text("spiller navn", key="userName")],
    [sg.Text("100 p", key="userPoints")],
    [sg.Button("Log ud")]
]

outCol = [
    [sg.Text("Log ind")],
    [sg.Text("for at gemme dine point")],
    [sg.Input(key="inputName")],
    [sg.Button("Ok")]
]

scoreboardCol = [
    [sg.Text("Top 10")],
]

layout = [
    [
        sg.Column(scoreboardCol, key="sbCol", justification="left"),
        sg.VSeperator(),
        sg.Column(outCol, key="outCol", justification="right"),
        sg.Column(inCol, key="inCol", visible=False, justification="right"),
    ]
]

window = sg.Window("LightRun", layout, no_titlebar=False, location=(0,0), size=(800,600), keep_on_top=True).Finalize()
window.Maximize()

# strip.queueSegment(segments[0])
strip.loopSegments(segments)
user.bindControls(pressRight, pressLeft)
buzz.write(False)

# mylcd = I2C_LCD_driver.lcd()
# mylcd.lcd_display_string("Hello World!", 1)

# Loop
while runLoop:
    startTime = time.time()

    event, values = window.read()
    if event is None:
        print("Du har lukket programmet")
        break
    if event == "Ok" and values["inputName"] != "":
        window.Element("outCol").Update(visible=False)
        window.Element("inCol").Update(visible=True)
    if event == "Log ud":
        window.Element("outCol").Update(visible=True)
        window.Element("inCol").Update(visible=False)

    if startGame:
        strip.update()
    else:
        startGame = btn.pressed()
        if startGame:
            pressLed.write(False)
        else:
            pressLed.write(tick % 2)
        
        if ENABLENAME:
            print(input("Enter name: "))
    
    user.update()

    tick += 1
    # print("frame tid:", time.time() - startTime)
    time.sleep(max(LOOPSPEED - (time.time() - startTime), 0))

window.close()



# https://tutorials-raspberrypi.com/how-to-control-a-raspberry-pi-ws2801-rgb-led-strip/