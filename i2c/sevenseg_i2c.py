from time import sleep

from i2c import SMBus


class SevenSegDisplay:
    ADDR = 0x70
    BLINK_CMD = 0x80
    BLINK_DISPLAY_ON = 0x01
    CMD_BRIGHTNESS = 0xE0
    COLON = 0x02
    CHARMAP = {
        '0': 0x3F,
        '1': 0x06,
        '2': 0x5B,
        '3': 0x4F,
        '4': 0x66,
        '5': 0x6D,
        '6': 0x7D,
        '7': 0x07,
        '8': 0x7F,
        '9': 0x6F,
        'a': 0x77,
        'b': 0x7C,
        'c': 0x39,
        'd': 0x5E,
        'e': 0x79,
        'f': 0x71}

    def __init__(self, bus):
        self.bus = bus
        self.chars = bytearray(4)
        self.dots = [False] * 4
        self.colon = False
        self.buf = [0] * 5

    def set_digits(self, digits):
        if len(digits) != 4:
            return
        for i, c in enumerate(digits):
            self.chars[i] = self.CHARMAP[c]

    def update(self):
        self.buf = []
        for i in range(4):
            self.buf.append((self.dots[i] << 7) | self.chars[i])
            self.buf.append(0)
            if i == 1:
                self.buf.append(self.COLON if self.colon else 0)
                self.buf.append(0)
        self.buf.extend([0] * 6)
        # print(self.buf)
        self.bus.write_i2c_block_data(self.ADDR, 0, self.buf)

    def begin(self):
        self.write_byte(0x21)  # start oscillator
        self.blink_rate(0)
        self.set_brightness(15)

    def write_byte(self, byte: hex):
        self.bus.write_byte(self.ADDR, byte)

    def set_brightness(self, level):
        level = 0 if level > 15 else level
        self.write_byte(self.CMD_BRIGHTNESS | level)

    def blink_rate(self, rate=0):
        rate = rate if rate <= 3 else 0
        self.write_byte(self.BLINK_CMD | self.BLINK_DISPLAY_ON | (rate << 1))


if __name__ == '__main__':
    bus = SMBus(1)
    sevenseg = SevenSegDisplay(bus)
    sevenseg.begin()
    # sevenseg.blink_rate(1)
    # sevenseg.dots = [True]*4
    # sevenseg.colon = True
    for n in range(1000):
        s = str(n).rjust(4, '0')
        # s = '2980'
        sevenseg.set_digits(s)
        sevenseg.update()
        sleep(.01)

    sevenseg.set_digits('beef')
    sevenseg.update()
