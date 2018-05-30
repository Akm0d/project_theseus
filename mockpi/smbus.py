#!/usr/bin/env python3
import logging

from multiprocessing import Manager, Process
from struct import unpack
from typing import List, Dict

log = logging.getLogger(__name__)


class MockBus(object):
    # The total number of registers
    REGISTERS = 0xff
    multi_process_dictionary = Manager().dict()

    def __init__(self, bus: int = None):
        log.debug("Initializing mock SMBus")
        self.bus = bus

    @property
    def messages(self) -> Dict[hex, bytearray]:
        return self.multi_process_dictionary

    def read_byte(self, address: hex) -> hex:
        return unpack('>BL', self.messages[address])

    def write_byte(self, address: hex, data: hex):
        self.messages[address] = bytearray(str(data).encode())

    def read_byte_data(self, address: hex, register: int) -> hex:
        """Read a single word from a designated register."""
        self._create_reg_if_not_exists(address)
        return self.messages[address][register]

    def write_byte_data(self, address: hex, register: hex, value: hex):
        """Write a single byte to a designated register."""
        self._create_reg_if_not_exists(address)
        self.messages[address][register] = value

    def read_i2c_block_data(self, address: hex, start_register: hex, buffer: int) -> hex:
        self._create_reg_if_not_exists(address)
        return int.from_bytes(self.messages[address][start_register: start_register + buffer], byteorder='big',
                              signed=False)

    def write_i2c_block_data(self, address: hex, start_register: hex, data: List[ord]):
        self._create_reg_if_not_exists(address)
        for reg, value in enumerate(data):
            self.messages[address][start_register + reg] = value

    def _create_reg_if_not_exists(self, address: hex):
        if self.messages.get(address, None) is None:
            self.messages[address] = bytearray(self.REGISTERS)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    from time import sleep


    def foo():
        for i in range(1, 5):
            MockBus().write_byte_data(address=0, register=0x1, value=i)
            print(MockBus().messages)


    Process(target=foo).start()

    sleep(.1)

    bar = MockBus()
    print(bar.read_word_data(0x1, 0x1))
    print(bar.messages)
