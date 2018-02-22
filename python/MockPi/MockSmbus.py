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

from mock import Mock, patch


class MockSMBus(object):
    # Mock the smbus.SMBus class to record all data written to specific
    # addresses and registers in the _written member.
    def __init__(self):
        # _written will store a dictionary of address to register dictionary.
        # Each register dictionary will store a mapping of register value to
        # an array of all written values (in sequential write order).
        self._written = {}
        self._read = {}

    def _write_register(self, address, register, value):
        self._written.setdefault(address, {}).setdefault(register, []).append(value)

    def _read_register(self, address, register):
        return self._read.get(address).get(register).pop(0)

    def write_byte_data(self, address, register, value):
        self._write_register(address, register, value)

    def write_word_data(self, address, register, value):
        self._write_register(address, register, value >> 8 & 0xFF)
        self._write_register(address, register + 1, value & 0xFF)

    def write_i2c_block_data(self, address, register, values):
        for i, value in enumerate(values):
            self._write_register(address, register + i, value & 0xFF)

    def read_byte_data(self, address, register):
        return self._read_register(address, register)

    def read_word_data(self, address, register):
        high = self._read_register(address, register)
        low = self._read_register(address, register + 1)
        return (high << 8) | low

    def read_i2c_block_data(self, address, length):
        return [self._read_register(address + i) for i in range(length)]


def create_device(address, busnum):
    # Mock the smbus module and inject it into the global namespace so the
    # Adafruit_GPIO.I2C module can be imported.  Also inject a mock SMBus
    # instance to be returned by smbus.SMBus function calls.
    smbus = Mock()
    mockbus = MockSMBus()
    smbus.SMBus.return_value = mockbus
    with patch.dict('sys.modules', {'smbus': smbus}):
        import Adafruit_GPIO.I2C as I2C
        return (I2C.Device(address, busnum), smbus, mockbus)


def safe_import_i2c():
    # Mock the smbus module and inject it into the global namespace so the
    # Adafruit_GPIO.I2C module can be imported.  The imported I2C module is
    # returned so global functions can be called on it.
    with patch.dict('sys.modules', {'smbus': Mock()}):
        import Adafruit_GPIO.I2C as I2C
        return I2C
