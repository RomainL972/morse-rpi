#!/usr/bin/env python3
from time import sleep, time
import backends
import json
import sys

TIME_UNIT = 0.05
if len(sys.argv) > 1:
    TIME_UNIT = float(sys.argv[1])

def setup():
    backend_name = "binary-text"
    if len(sys.argv) >=3:
        backend_name = sys.argv[2]
    return backends.getBackend(backend_name)(TIME_UNIT)

def loop(backend):
    string = input("String : ") + "\n"
    code = backend.encode(string)
    with open("code.txt", "w") as f:
        f.write(json.dumps(code))
    print("Number of parts :",len(code))
    total_time = 0
    for e in code:
        total_time += e["time"]
    print("Total time :",round(total_time, 2),"s")

if __name__ == '__main__':    # Program entrance
    print ('Program is starting ... \n')
    backend = setup()
    loop(backend)
