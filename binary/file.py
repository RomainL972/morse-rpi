from .common import BinaryCommon, MAX_PACKET_DATA_SIZE, LENGTH_HEADER_SIZE
import os

FILE_LENGTH_HEADER_SIZE = 24

class BinaryFile():
    def __init__(self, unit_time, debug=False):
        self.common = BinaryCommon(unit_time, debug)
        self.bits = ""
        self.file_size = 0
        self.file_name = ""
        self.unit_time = unit_time
        self.name = "binary-file"

    def encode(self, file_name):
        with open(file_name, "rb") as f:
            data = f.read()

        # Add filename
        data = file_name.encode() + b'\0' + data

        # Convert to binary and left-pad with zeros to form bytes
        binary_array = bin(int.from_bytes(data, byteorder='big'))[2:]
        binary_array = "0" * (8-len(binary_array)%8) + binary_array

        # Add length header
        length = bin(len(binary_array))[2:]
        print(f"Length : {length}")
        if len(length) > FILE_LENGTH_HEADER_SIZE:
            raise ValueError("File too big!")
        binary_array = length.zfill(FILE_LENGTH_HEADER_SIZE) + binary_array

        # Separate into chunks
        chunks = [binary_array[i:i+MAX_PACKET_DATA_SIZE] for i in range(0,len(binary_array),MAX_PACKET_DATA_SIZE)]

        for chunk in chunks:
            print("Chunk : ",chunk)

        return self.common.chunks_to_signal(chunks)

    def decode_file_name(self):
        print(f"Decoding file name {self.bits}")
        self.file_name = self.common.bin_to_bytes(self.bits[:-8]).decode()

    def decode_file_data(self):
        os.mkdir("uploads")
        print("Writing result to uploads/" + self.file_name)
        with open("uploads/" + self.file_name, "wb") as f:
            f.write(self.common.bin_to_bytes(self.bits))

    def parse_signal(self, led_state):
        bit = self.common.parse_signal(led_state)

        if bit:
            self.bits += bit
            if self.file_size == 0:
                if len(self.bits) == FILE_LENGTH_HEADER_SIZE:
                    self.file_size = int(self.bits, 2)
                    self.bits = ""
            elif not self.file_name:
                if len(self.bits) > 8 and len(self.bits)%8==0 and self.bits[-8:] == "0" * 8:
                    self.decode_file_name()
                    self.file_size -= len(self.bits)
                    self.bits = ""
            elif len(self.bits) == self.file_size:
                self.decode_file_data()
                self.bits = ""
                self.file_size = 0
                self.file_name = ""
