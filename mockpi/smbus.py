#!/usr/bin/env python3
from multiprocessing import Manager, Process
from struct import unpack
from typing import List

manager = Manager()
shared_dict = manager.dict()


class MockBus(object):
    # The total number of registers
    REGISTERS = 0xff

    def __init__(self, bus: int = None):
        self.bus = bus
        self.messages = shared_dict

    def read_byte(self, address: hex) -> hex:
        return unpack('>BL', self.messages[address])

    def write_byte(self, address: hex, data: hex):
        self._create_reg_if_not_exists(address)
        for reg, byte in enumerate(bytearray(str(data).encode())):
            self.messages[address][reg] = byte

    def read_byte_data(self, address: hex, register: int) -> hex:
        """Read a single word from a designated register."""
        self._create_reg_if_not_exists(address)
        return self.messages[address][register]

    def write_byte_data(self, address: hex, register: hex, value: hex):
        """Write a single byte to a designated register."""
        self._create_reg_if_not_exists(address)
        self.messages[address][register] = value

    def read_i2c_block_data(self, address: hex, start_register: hex, buffer: int) -> bytearray:
        self._create_reg_if_not_exists(address)
        return bytearray(self.messages[address][start_register: start_register + buffer])

    def write_i2c_block_data(self, address: hex, start_register: hex, data: List[ord]):
        self._create_reg_if_not_exists(address)
        for reg, value in enumerate(data):
            self.messages[address][start_register + reg] = value

    def _create_reg_if_not_exists(self, address: hex):
        if self.messages.get(address, None) is None:
            self.messages[address] = manager.list(bytearray(self.REGISTERS))


if __name__ == "__main__":
    from time import sleep
    master = 0
    length = 5


    def write_i2c_thread():
        for i, x in enumerate(range(length)):
            MockBus().write_byte_data(address=master, register=i, value=0xf)
            print(MockBus().read_i2c_block_data(master, 0x0, length))


    Process(target=write_i2c_thread).start()

    sleep(.1)

    print(MockBus().read_i2c_block_data(master, 0, length))
