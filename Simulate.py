#!/usr/bin/env python3
import backends
import json
import time
import sys
from debug import Debug

TIME_UNIT = 0.05
if len(sys.argv) > 1:
    TIME_UNIT = float(sys.argv[1])

def setup():
    return backends.getBackend("binary")(TIME_UNIT)

def mprint(message):
    print(message, end='', flush=True)

def loop(backend):
    with open("code.txt", "r") as f:
        code = json.load(f)

    #print(backend)

    backend.parse_signal(False)
    time.sleep(TIME_UNIT*10)

    for i in code:
        start_time = time.time()
        char = backend.parse_signal(i["state"])
        if char:
            mprint(char)
        while start_time+i["time"]>time.time():
            pass

if __name__ == '__main__':   # Program entrance
    print ('Program is starting ... ')
    backend = setup()
    loop(backend)
    if isinstance(backend, Debug):
        backend.write_results()
