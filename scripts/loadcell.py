#!/usr/bin/env python3
import RPi.GPIO as GPIO  # import GPIO
from loadcell_class import HX711  # import the class HX711


while True:
    GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
    hx = HX711(dout_pin=13, pd_sck_pin=11)  # create an object
    print(hx._read())  # get raw data reading from hx711
    GPIO.cleanup()

