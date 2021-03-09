from .common import BinaryCommon, MAX_PACKET_DATA_SIZE, LENGTH_HEADER_SIZE

class BinaryText():
    def __init__(self, unit_time, debug=False):
        self.common = BinaryCommon(unit_time, debug)
        self.bits = ""
        self.byte_size = 0
        self.unit_time = unit_time
        self.name = "binary-text"

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

        return self.common.chunks_to_signal(chunks)

    def decode(self):
        # print("Decoding :",self.bits)
        return self.common.bin_to_bytes(self.bits).decode()

    def parse_signal(self, led_state):
        bit = self.common.parse_signal(led_state)
        return_val = ""

        if bit:
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

        return return_val
