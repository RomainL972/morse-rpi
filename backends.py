from binary.text import BinaryText
from binary.file import BinaryFile
from morse import Morse
from debug import Debug

def getBackend(backend):
    if backend == "binary-text":
        return BinaryText
    elif backend == "binary-file":
        return BinaryFile
    elif backend == "morse":
        return Morse
    elif backend == "debug":
        return Debug
    else:
        raise Exception(f"Backend {backend} doesn't exist")
