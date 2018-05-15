#!/usr/bin/env python3
import logging

from multiprocessing import Manager, Process
from typing import List

log = logging.getLogger(__name__)


class MockBus(object):
    messages = Manager().dict()

    # Mock the smbus.SMBus class to record all data written to specific
    # addresses and registers in the _written member.
    def __init__(self, bus: int = None):
        log.debug("Initializing mock SMBus")
        # Unused value, there is only one bus
        self.addr = bus

    def _set_addr(self, addr):
        if self.addr != addr:
            self.addr = addr

    def write_byte_data(self, i2c_addr, register: int, value):
        """Write a single byte to a designated register."""
        # print("Address: {}  Register: {}  Value: {}".format(i2c_addr, register, value))
        self._create_queue_if_none(register)
        log.debug("Register: {} value: {}".format(register, value))
        new_list = [value]
        new_list.extend(self.messages[register])
        self.messages[register] = new_list

    def read_word_data(self, i2c_addr, register: int):
        """Read a single word from a designated register."""
        self._create_queue_if_none(register)
        result = self.messages[register].pop()
        self.messages[register] = self.messages[register][:-1]
        return result

    def write_i2c_block_data(self, address: hex, start_register: hex, data: List[ord]):
        for i, d in enumerate(data):
            register = start_register + i
            self._create_queue_if_none(register)
            new_list = [d]
            new_list.extend(self.messages[register])
            self.messages[register] = new_list

    def _create_queue_if_none(self, register: int):
        if self.messages.get(register, None) is None:
            log.debug("Created register: {}".format(register))
            self.messages[register] = list()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    from time import sleep


    def foo():
        for i in range(1, 5):
            MockBus().write_byte_data(i2c_addr=0, register=0x1, value=i)
            print(MockBus().messages)

    Process(target=foo).start()

    sleep(.1)

    bar = MockBus()
    print(bar.read_word_data(0x1, 0x1))
    print(bar.messages)
