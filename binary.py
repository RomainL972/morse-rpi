import time
from enum import Enum

LENGTH_HEADER_SIZE = 7
MAX_PACKET_DATA_SIZE = 2**(LENGTH_HEADER_SIZE-1)

class State(Enum):
    IDLE = 0
    STARTING = 1
    STARTED = 2

class Binary():
    def __init__(self, unit_time):
        self.unit_time = unit_time

        # For signal parsing
        self.state = State.IDLE
        self.last_time = time.time()
        self.bits = ""
        self.bits_left = 0
        self.byte_size = 0

        self.begin_time = 0
        self.i = 0

        self.first = True

    def encode(self, string):
        chunks = []
        chunk = ""
        for char in string:
            binary = ""
            for byte in char.encode():
                binary += bin(byte)[2:].zfill(8)

            if len(chunk) + len(binary) > MAX_PACKET_DATA_SIZE:
                chunks.append(chunk)
                chunk = ""
            chunk += binary
        chunks.append(chunk)
        # print("result :",bits)

        # chunk_size = MAX_PACKET_DATA_SIZE
        # chunks = ["".join(bits[i:i+chunk_size]) for i in range(0, len(bits), chunk_size)]

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

    def decode(self):
        # print("Decoding :",self.bits)
        return int(self.bits, 2).to_bytes(len(self.bits)//8, "big").decode()

    def parse_signal(self, led_state):
        current_time = time.time()
        units = (current_time - self.last_time) / self.unit_time

        if self.state == State.IDLE and units > 2:
            self.first = True

        if self.state == State.IDLE and (not led_state or units <1):
            return

        if units >= 1:
            # print(self.i,": State :",self.state,", bit ","0" if led_state else "1","at",time.time()-self.begin_time)
            self.i += 1
            if self.state == State.IDLE and led_state:
                self.state = State.STARTING
                if self.first:
                    self.last_time = current_time + 0.5 * self.unit_time
                    self.first = False
                else:
                    self.last_time = current_time
                if not self.begin_time:
                    self.begin_time = time.time()
                return

            # print("State :", "0" if led_state else "1","at",time.time()-self.begin_time)
            bit = "0" if led_state else "1"
            return_val = ""

            if self.state == State.STARTING:
                self.bits += bit
                if len(self.bits) == LENGTH_HEADER_SIZE:
                    self.bits_left = int(self.bits, 2)
                    self.state = State.STARTED
                    self.bits = ""
                    # print("Packet size :",self.bits_left)

            elif self.state == State.STARTED:
                self.bits += bit
                if self.byte_size <= 0:
                    if bit == "1":
                        self.byte_size -= 1
                    else:
                        self.byte_size *= -8
                        if self.byte_size == 0:
                            self.byte_size += 8
                elif len(self.bits) == self.byte_size:
                    return_val = self.decode()
                    self.bits = ""
                    self.byte_size = 0

                self.bits_left -= 1
                if self.bits_left <= 0:
                    self.state = State.IDLE
                    self.byte_size = 0
                    self.bits = ""

            self.last_time += self.unit_time

            return return_val
