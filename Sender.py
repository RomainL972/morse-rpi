#!/usr/bin/env python3
########################################################################
# Filename    : Blink.py
# Description : Basic usage of GPIO. Let led blink.
# auther      : www.freenove.com
# modification: 2019/12/28
########################################################################
import RPi.GPIO as GPIO
from time import sleep
from morse import Morse

ledPin = 11    # define ledPin

import sys

MORSE_UNIT = 0.05
if len(sys.argv) > 1:
    MORSE_UNIT = float(sys.argv[1])

def setup():
    GPIO.setmode(GPIO.BOARD)       # use PHYSICAL GPIO Numbering
    GPIO.setup(ledPin, GPIO.OUT)   # set the ledPin to OUTPUT mode
    GPIO.output(ledPin, GPIO.LOW)  # make ledPin output LOW level
    print ('using pin%d'%ledPin)
    morse_manager = Morse(MORSE_UNIT)
    return morse_manager

def set_led(mode, sleep_time):
    GPIO.output(ledPin, mode)
    sleep(sleep_time)


def loop(morse_manager):
    while True:
        string = input("String : ")
        code = morse_manager.encode(string)
        print("Number of parts :",len(code))
        total_time = 0
        for e in code:
            if e["state"]:
                state = GPIO.HIGH
            else:
                state = GPIO.LOW
            total_time += e["time"]
            set_led(state, e["time"])
        print("Total time :",round(total_time, 2),"s")

def destroy():
    GPIO.cleanup()                      # Release all GPIO

if __name__ == '__main__':    # Program entrance
    print ('Program is starting ... \n')
    morse_manager = setup()
    try:
        loop(morse_manager)
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        destroy()
