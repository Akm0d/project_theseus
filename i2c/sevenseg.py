import logging
from multiprocessing import Lock
from typing import List

from smbus2 import SMBus

from i2c.i2c_module import I2CModule

logger = logging.getLogger(__name__)


class SevenSeg(I2CModule):
    _lock = Lock()
    NUM_DOTS = 4
    ADDRESS = I2C.SEVENSEG.value
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
        'f': 0x71
    }

    def __init__(self, bus: SMBus, address: hex = 0x70, blink_rate: int = 0, brightness: hex = 0):
        """
        :param bus:
        :param blink_rate:
        :param brightness:
        """
        super().__init__(bus, address)
        assert blink_rate >= 0, "Blink rate must be positive: {}".format(blink_rate)
        assert 0 <= brightness <= 0xf, "Brightness level is out of range: {}".format(brightness)
        # start oscillator
        self.write(0x21)

        # Initialize Seven Segment Display
        self.blink_rate(blink_rate)
        self.brightness(brightness)

    def write(self, byte: hex):
        with self._lock:
            self.bus.write_byte(self.ADDRESS, byte)

    def sevenseg(self, value: hex, dots: List[bool] = None, colon: bool = True):
        """
        :param colon: True if a colon should be written, else false
        :param dots: A list of 4 booleans representing the 4 dots that should be written
        :param value: A 4 digit hex value to write to the seven segment display
        """
        # Type checking and input sensitization
        assert 0 <= value <= 0xffff, "'{}' is out of the range of the seven segment display".format(value)
        if dots is None:
            dots = list()
        assert len(dots) <= 4, "There are only 4 dots on the display"

        # Add to the dots array until there are enough
        while len(dots) < 4:
            dots.append(False)

        chars = [self.CHARMAP[c] for c in str(hex(value))[2:].zfill(4)]

        # Build the buffer that sends characters to the device
        buffer = []
        for i in range(4):
            buffer.append((dots[i] << 7) | chars[i])
            buffer.append(0)
            if i == 1:
                buffer.append(self.COLON if colon else 0)
                buffer.append(0)

        try:
            with self._lock:
                self.bus.write_i2c_block_data(self.ADDRESS, 0, buffer)
        except OSError as c:
            logger.error("{}:{}".format(c, hex(value)))

    def brightness(self, level: int):
        level = 0 if level > 15 else level
        self.write(self.CMD_BRIGHTNESS | level)

    def blink_rate(self, rate: int = 0):
        rate = rate if rate <= 3 else 0
        self.write(self.BLINK_CMD | self.BLINK_DISPLAY_ON | (rate << 1))


if __name__ == '__main__':
    from time import sleep

    kit = SevenSeg(SMBus(1), brightness=3)

    while True:
        for n in range(0xffff):
            kit.sevenseg(value=n)
            sleep(.1)
