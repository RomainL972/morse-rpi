#!/usr/bin/env python3
########################################################################
# Filename    : Blink.py
# Description : Basic usage of GPIO. Let led blink.
# auther      : www.freenove.com
# modification: 2019/12/28
########################################################################
import RPi.GPIO as GPIO
from time import sleep, time
from binary import Binary
from morse import Morse

ledPin = 11    # define ledPin
begin_time = time()
i = 0

import sys

TIME_UNIT = 0.05
if len(sys.argv) > 1:
    TIME_UNIT = float(sys.argv[1])

def setup():
    GPIO.setmode(GPIO.BOARD)       # use PHYSICAL GPIO Numbering
    GPIO.setup(ledPin, GPIO.OUT)   # set the ledPin to OUTPUT mode
    GPIO.output(ledPin, GPIO.LOW)  # make ledPin output LOW level
    print ('using pin%d'%ledPin)
    if len(sys.argv) < 3 or sys.argv[2] == "binary":
        backend = Binary(TIME_UNIT)
    elif len(sys.argv) >= 3 and sys.argv[2] == "morse":
        backend = Morse(TIME_UNIT)
    else:
        print("Please choose [binary] or morse for backend")
    return backend

def set_led(mode, sleep_time):
    global i
    start_time = time()
    GPIO.output(ledPin, mode)
    # print(i,": Set ","0" if mode else "1","at",time()-begin_time)
    i += 1
    while start_time+sleep_time>time():
        pass


import json
def loop(backend):
    global begin_time
    while True:
        string = input("String : ") + "\n"
        code = backend.encode(string)
        with open("code.txt", "w") as f:
            f.write(json.dumps(code))
        print("Number of parts :",len(code))
        total_time = 0
        begin_time = time()
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
    backend = setup()
    try:
        loop(backend)
    finally:   # Press ctrl-c to end the program.
        destroy()
