# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


class MockGPIO:
    BCM = 11
    BOARD = 10
    BOTH = 33
    FALLING = 32
    HARD_PWM = 43
    HIGH = 1
    I2C = 42
    IN = 1
    LOW = 0
    OUT = 0
    PUD_DOWN = 21
    PUD_OFF = 20
    PUD_UP = 22
    RISING = 31
    RPI_INFO = {
        'P1_REVISION': 3,
        'REVISION': 'a01041',
        'TYPE': 'Pi 2 Model B',
        'MANUFACTURER': 'Sony',
        'PROCESSOR': 'BCM2836',
        'RAM': '1024M'
    }
    RPI_REVISION = 3
    SERIAL = 40
    SPI = 41
    UNKNOWN = -1
    VERSION = '0.6.3'

    def __init__(self):
        self.pin_mode = {}
        self.pin_written = {}
        self.pin_read = {}

    def setup(self, pin, mode, pull_up_down=0):
        self.pin_mode[pin] = mode

    def output(self, pin, bit):
        self.pin_written.setdefault(pin, []).append(1 if bit else 0)

    def input(self, pin):
        if pin not in self.pin_read:
            raise RuntimeError('No mock GPIO data to read for pin {0}'.format(pin))
        return self.pin_read[pin].pop(0) == 1

    def wait_for_edge(self, pin, edge):
        pass

    def cleanup(self, pin=None):
        pass
