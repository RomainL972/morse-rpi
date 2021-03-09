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
    backend_name = "binary-text"
    if len(sys.argv) > 2:
        backend_name = sys.argv[2]
    if backend_name == "binary-text" or backend_name == "binary-file":
        return backends.getBackend(backend_name)(TIME_UNIT, debug=True)
    else:
        return backends.getBackend(backend_name)(TIME_UNIT)

def mprint(message):
    print(message, end='', flush=True)

def loop(backend):
    with open("code.txt", "r") as f:
        code = json.load(f)

    #print(backend)

    backend.parse_signal(False)
    time.sleep(TIME_UNIT*10)

    for i in code:
        char = backend.parse_signal(i["state"])
        if char:
            mprint(char)

if __name__ == '__main__':   # Program entrance
    print ('Program is starting ... ')
    backend = setup()
    loop(backend)
    if isinstance(backend, Debug):
        backend.write_results()
