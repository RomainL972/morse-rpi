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

adc = ADCDevice() # Define an ADCDevice class object

MORSE_UNIT = 0.05
if len(sys.argv) > 1:
    MORSE_UNIT = float(sys.argv[1])
SLEEP_TIME = 0.001

MORSE_TABLE = {   '-': 'T',
    '--': 'M',
    '---': 'O',
    '-----': '0',
    '----.': '9',
    '---..': '8',
    '--.': 'G',
    '--.-': 'Q',
    '--..': 'Z',
    '--..--': ', ',
    '--...': '7',
    '-.': 'N',
    '-.-': 'K',
    '-.--': 'Y',
    '-.--.': '(',
    '-.--.-': ')',
    '-.-.': 'C',
    '-..': 'D',
    '-..-': 'X',
    '-..-.': '/',
    '-...': 'B',
    '-....': '6',
    '-....-': '-',
    '.': 'E',
    '.-': 'A',
    '.--': 'W',
    '.---': 'J',
    '.----': '1',
    '.--.': 'P',
    '.-.': 'R',
    '.-.-.-': '.',
    '.-..': 'L',
    '..': 'I',
    '..-': 'U',
    '..---': '2',
    '..--..': '?',
    '..-.': 'F',
    '...': 'S',
    '...-': 'V',
    '...--': '3',
    '....': 'H',
    '....-': '4',
    '.....': '5'}

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
    global p
    
def mprint(message):
    print(message, end='', flush=True)

def decode(code):
    return MORSE_TABLE.get(code)

def loop():
    #i = 0
    led_on = 0
    old_led_on = 0
    last_time = time.time()
    started = 0
    letter = ""
    #print("State : ",led_on)
    start = time.time()
    while True:
        value = adc.analogRead(0)    # read the ADC value of channel 0
        if len(sys.argv) > 2:
            print("value : ",value,", time :",time.time()-start)
        if value < 45:
            led_on = 1
        elif value >= 45:
            led_on = 0
        #else:
        #    print("Unknown")
        i = time.time()  
        units = round((i - last_time) / MORSE_UNIT)
        if started and units > 7 and letter:
            mprint(decode(letter))
            letter = ""
            started = 0

        elif led_on != old_led_on:
            #print("Units : ", (i - last_time) / MORSE_UNIT ,"s")
            #print("\nState : ",led_on)

            #print("started :",started)
            if started == 0 or units > 7:
                started = 1
                if letter:
                    mprint(decode(letter))
                letter = ""
                mprint("\n")
            else:
                #print("Checking state")
                if units == 1 and not old_led_on:
                    #print("small pause")
                    pass
                elif units == 3 and not old_led_on:
                    mprint(decode(letter))
                    letter = ""
                elif units == 7 and not old_led_on:
                    mprint(decode(letter))
                    mprint(" ")
                    letter = ""
                elif units == 1 and old_led_on:
                    letter += "."
                    #mprint(".")
                elif units == 3 and old_led_on:
                    letter += "-"
                    #mprint("-")

            last_time = i
            old_led_on = led_on
        #time.sleep(SLEEP_TIME)
        #i += 1

def destroy():
    adc.close()
    
if __name__ == '__main__':   # Program entrance
    print ('Program is starting ... ')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
        
    
