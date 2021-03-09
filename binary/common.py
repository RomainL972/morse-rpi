import time
from enum import Enum

LENGTH_HEADER_SIZE = 7
MAX_PACKET_DATA_SIZE = 2**(LENGTH_HEADER_SIZE-1)

class State(Enum):
    IDLE = 0
    STARTING = 1
    STARTED = 2

class BinaryCommon():
    def __init__(self, unit_time, debug=False):
        self.unit_time = unit_time
        self.debug = debug

        # For signal parsing
        self.state = State.IDLE
        self.last_time = time.time()
        self.bits = ""
        self.bits_left = 0

        self.first = True
        self.average = {"sum":0,"n":0}

    def chunks_to_signal(self, chunks):
        result = []
        for chunk in chunks:
            if len(chunk) > MAX_PACKET_DATA_SIZE:
                raise Exception("WTF???")
            # Start signal
            result.append({"state": True, "time": self.unit_time})
            # Length header
            chunk = bin(len(chunk))[2:].zfill(LENGTH_HEADER_SIZE) + chunk
            # print("Chunk :",chunk)

            for bit in chunk:
                result.append({
                    "state": True if (bit == "0") else False,
                    "time": self.unit_time
                })

        # Shutdown LED at the end
        result.append({"state": False, "time": 0})

        return result

    def bin_to_bytes(self, bin):
        return int(bin, 2).to_bytes(len(bin)//8, "big")

    def parse_signal(self, led_state):
        current_time = time.time()
        units = (current_time - self.last_time) / self.unit_time

        if self.state == State.IDLE and units > 2:
            self.first = True

        if self.state == State.IDLE and (not led_state or units <1) and not self.debug:
            return

        if units > 0 and units < 1:
            self.average["sum"] += led_state
            self.average["n"] += 1
        if units >= 1 or self.debug:
            if self.average["n"] > 0 and not self.debug:
                average = self.average["sum"] / self.average["n"]
                self.average["sum"] = self.average["n"] = 0
                if not self.first:
                    led_state = average == 1

            if self.state == State.IDLE and led_state:
                self.state = State.STARTING
                if self.first:
                    self.last_time = current_time + self.unit_time
                    self.first = False
                else:
                    self.last_time = current_time
                return

            # print("State :", "0" if led_state else "1","at",time.time()-self.begin_time)
            bit = "0" if led_state else "1"
            return_val = None

            if self.state == State.STARTING:
                self.bits += bit
                if len(self.bits) == LENGTH_HEADER_SIZE:
                    self.bits_left = int(self.bits, 2)
                    self.state = State.STARTED
                    self.bits = ""
                    # print("Packet size :",self.bits_left)

            elif self.state == State.STARTED:
                return_val = bit
                self.bits_left -= 1
                if self.bits_left <= 0:
                    self.state = State.IDLE
                    self.byte_size = 0
                    self.bits = ""

            self.last_time += self.unit_time

            return return_val
