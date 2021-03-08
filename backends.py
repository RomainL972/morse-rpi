from binary import Binary
from morse import Morse
from debug import Debug

def getBackend(backend):
    if backend == "binary":
        return Binary
    elif backend == "morse":
        return Morse
    elif backend == "debug":
        return Debug
    else:
        raise Exception(f"Backend {backend} doesn't exist")
