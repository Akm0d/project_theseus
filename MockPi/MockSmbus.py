#!/usr/bin/env python3
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

import logging
import struct
from ctypes import c_int, c_uint8, POINTER, Structure
from multiprocessing import Manager, Process
from queue import Queue, Empty
from typing import List

log = logging.getLogger(__name__)

I2C_SLAVE = 0x0703
I2C_SMBUS = 0x0720
I2C_SMBUS_WRITE = 0
I2C_SMBUS_READ = 1
I2C_SMBUS_BYTE_DATA = 2

LP_c_uint8 = POINTER(c_uint8)


class i2c_smbus_msg(Structure):
    _fields_ = [
        ('read_write', c_uint8),  # Should be c_char, but c_uint8 is the
        # same size is makes it easier to
        # support both Python 2.7 and 3.x.
        ('command', c_uint8),
        ('size', c_int),
        ('data', LP_c_uint8)]

    __slots__ = [name for name, type in _fields_]


class MockBus(object):
    manager = Manager()
    fd = manager.dict()

    # Mock the smbus.SMBus class to record all data written to specific
    # addresses and registers in the _written member.
    def __init__(self, bus: int = None):
        log.debug("Initializing mock SMBus")
        self.addr = 0
        self.messages = {self.addr: Queue()}

    def _set_addr(self, addr):
        if self.addr != addr:
            self.addr = addr

    def write_byte_data(self, i2c_addr, register, value):
        """Write a single byte to a designated register."""
        # print("Address: {}  Register: {}  Value: {}".format(i2c_addr, register, value))
        byte_value = c_uint8(value)
        data_pointer = LP_c_uint8(byte_value)
        msg = i2c_smbus_msg(
            read_write=I2C_SMBUS_WRITE, command=register,
            size=I2C_SMBUS_BYTE_DATA, data=data_pointer)

        if self.messages.get(i2c_addr, None) is None:
            self.messages[i2c_addr] = Queue()

        # TODO Read the mesages put in the queue in a thread and generate responses
        self.messages[i2c_addr].put(msg)

    def read_word_data(self, i2c_addr, register):
        """Read a single word from a designated register."""
        try:
            msg = self.messages[self.addr].get_nowait()
            [result] = struct.unpack("@b", msg)
        except Empty:
            return

        return result

    def write_i2c_block_data(self, address: hex, start_register: hex, data: List[ord]):
        pass


if __name__ == "__main__":
    from time import sleep


    def foo():
        MockBus().fd["a"] = 1


    Process(target=foo).start()

    sleep(.1)

    bar = MockBus()
    print(bar.fd)
