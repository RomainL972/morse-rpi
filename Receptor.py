#!/usr/bin/env python3
#############################################################################
# Filename    : Nightlamp.py
# Description : Control LED with Photoresistor
# Author      : www.freenove.com
# modification: 2020/03/09
########################################################################
import RPi.GPIO as GPIO
import time
from ADCDevice import *
import sys
from binary import Binary as Morse
# from debug import Debug as Morse

adc = ADCDevice() # Define an ADCDevice class object

MORSE_UNIT = 0.05
if len(sys.argv) > 1:
    MORSE_UNIT = float(sys.argv[1])

def setup():
    global adc
    if(adc.detectI2C(0x48)): # Detect the pcf8591.
        adc = PCF8591()
    elif(adc.detectI2C(0x4b)): # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
        "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
        "Program Exit. \n");
        exit(-1)
    return Morse(MORSE_UNIT)

def mprint(message):
    print(message, end='', flush=True)

def loop(morse):
    while True:
        value = adc.analogRead(0)    # read the ADC value of channel 0
        if len(sys.argv) > 2:
            print("value : ",value,", time :",time.time()-start)

        if value < 30:
            led_on = True
        elif value >= 30:
            led_on = False

        char = morse.parse_signal(led_on)
        if char:
            mprint(char)


def destroy():
    adc.close()

if __name__ == '__main__':   # Program entrance
    print ('Program is starting ... ')
    morse = setup()
    try:
        loop(morse)
    finally:  # Press ctrl-c to end the program.
        destroy()
