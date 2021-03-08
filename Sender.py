#!/usr/bin/env python3
########################################################################
# Filename    : Blink.py
# Description : Basic usage of GPIO. Let led blink.
# auther      : www.freenove.com
# modification: 2019/12/28
########################################################################
import RPi.GPIO as GPIO
from time import sleep, time
import backends

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
    
    backend_name = "binary"
    if len(sys.argv) >=3:
        backend_name = sys.argv[2]
    return backends.getBackend(backend_name)(TIME_UNIT)

def set_led(mode, sleep_time):
    global i
    start_time = time()
    GPIO.output(ledPin, mode)
    # print(i,": Set ","0" if mode else "1","at",time()-begin_time)
    i += 1
    while start_time+sleep_time>time():
        pass


def loop(backend):
    global begin_time
    while True:
        string = input("String : ") + "\n"
        code = backend.encode(string)
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
