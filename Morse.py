#!/usr/bin/env python3
########################################################################
# Filename    : Blink.py
# Description : Basic usage of GPIO. Let led blink.
# auther      : www.freenove.com
# modification: 2019/12/28
########################################################################
import RPi.GPIO as GPIO
from time import sleep

ledPin = 11    # define ledPin

MORSE_CODE_DICT = { 'A':'.-', 'B':'-...', 
                    'C':'-.-.', 'D':'-..', 'E':'.', 
                    'F':'..-.', 'G':'--.', 'H':'....', 
                    'I':'..', 'J':'.---', 'K':'-.-', 
                    'L':'.-..', 'M':'--', 'N':'-.', 
                    'O':'---', 'P':'.--.', 'Q':'--.-', 
                    'R':'.-.', 'S':'...', 'T':'-', 
                    'U':'..-', 'V':'...-', 'W':'.--', 
                    'X':'-..-', 'Y':'-.--', 'Z':'--..', 
                    '1':'.----', '2':'..---', '3':'...--', 
                    '4':'....-', '5':'.....', '6':'-....', 
                    '7':'--...', '8':'---..', '9':'----.', 
                    '0':'-----', ', ':'--..--', '.':'.-.-.-', 
                    '?':'..--..', '/':'-..-.', '-':'-....-', 
                    '(':'-.--.', ')':'-.--.-'}

MORSE_UNIT = 0.02

def setup():
    GPIO.setmode(GPIO.BOARD)       # use PHYSICAL GPIO Numbering
    GPIO.setup(ledPin, GPIO.OUT)   # set the ledPin to OUTPUT mode
    GPIO.output(ledPin, GPIO.LOW)  # make ledPin output LOW level 
    print ('using pin%d'%ledPin)

def set_led(mode, sleep_time):
    GPIO.output(ledPin, mode)
    sleep(sleep_time)

def letter(letter):
    code = MORSE_CODE_DICT.get(letter.upper())
    if not code:
        return
    for part in code:
        if part == ".":
            time = 1
        elif part == "-":
            time = 3
        set_led(GPIO.HIGH, time*MORSE_UNIT)
        set_led(GPIO.LOW, MORSE_UNIT)

def word(word):
    for l in word:
        letter(l)
        sleep(2*MORSE_UNIT)

def convert(string):
    for w in string.split(" "):
        word(w)
        sleep(4*MORSE_UNIT)


def loop():
    while True:
        string = input("String : ")
        convert(string)
        #GPIO.output(ledPin, GPIO.HIGH)  # make ledPin output HIGH level to turn on led
        #print ('led turned on >>>')     # print information on terminal
        #time.sleep(0.2)                   # Wait for 1 second
        #GPIO.output(ledPin, GPIO.LOW)   # make ledPin output LOW level to turn off led
        #print ('led turned off <<<')
        #time.sleep(2)                   # Wait for 1 second

def destroy():
    GPIO.cleanup()                      # Release all GPIO

if __name__ == '__main__':    # Program entrance
    print ('Program is starting ... \n')
    setup()
    try:
        loop()
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        destroy()

