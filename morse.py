import time

MORSE_ENCODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}

MORSE_DECODE_DICT = {   '-': 'T',
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

class Morse():
    def __init__(self, unit_time):
        self.unit_time = unit_time

        # For signal parsing
        self.message_started = False
        self.last_time = time.time()
        self.last_state = False
        self.letter = ""

    def encode(self, string):
        result = []
        for word in string.split(" "):
            for letter in word:
                code = MORSE_ENCODE_DICT.get(letter.upper())
                if code:
                    for part in code:
                        if part == ".":
                            duration = 1
                        elif part == "-":
                            duration = 3
                        result.append({"state": True, "time": duration*self.unit_time})
                        result.append({"state": False, "time": self.unit_time})
                    result.append({"state": False, "time": self.unit_time*2})
            result.append({"state": False, "time": self.unit_time*4})
        return result

    def decode(self, code):
        return MORSE_DECODE_DICT.get(code)

    def parse_signal(self, state):
        current_time = time.time()
        char = None

        units = round((current_time - self.last_time) / self.unit_time)
        if self.message_started and units > 7:
            self.message_started = False
            if self.letter:
                char = self.decode(self.letter) + "\n"
                self.letter = ""
            else:
                char = "\n"

        elif state != self.last_state:
            if not self.message_started:
                self.message_started = True

            if units == 3 and not self.last_state:
                char = self.decode(self.letter)
                self.letter = ""
            elif units == 7 and not self.last_state:
                char = self.decode(self.letter) + " "
                self.letter = ""
            elif units == 1 and self.last_state:
                self.letter += "."
            elif units == 3 and self.last_state:
                self.letter += "-"

            self.last_state = state
            self.last_time = current_time

        return char
