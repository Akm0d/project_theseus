from array import array
from enum import IntEnum
from struct import unpack
from time import sleep
from typing import List, Union
import logging

from smbus2 import SMBus

from i2c.i2c_module import I2CModule


logger = logging.Logger(__name__)


class ReceptorRegisters(IntEnum):
    Conversion = 0x00,
    Alert = 0x01,
    Config = 0x02,
    CycleTime = 0x03,
    Data1Low = 0x04,
    Data1High = 0x05,
    Hyst1 = 0x06,
    Data2Low = 0x07,
    Data2High = 0x08,
    Hyst2 = 0x09,
    Data3Low = 0x0A,
    Data3High = 0x0B,
    Hyst3 = 0x0C,
    Data4Low = 0x0D,
    Data4High = 0x0E,
    Hyst4 = 0x0F


class ReceptorControl(I2CModule):
    RECEPTOR_COUNT = 6
    CHANNEL = [0x80, 0x90, 0xA0, 0xB0, 0xC0, 0xD0, 0xE0, 0xF0]
    CONFIG = [0x03, 0xF8]
    READ_ALL = 0x70
    THRESHOLD = 800
    # UNPACK_ALL = ''.join(['>'].extend(['H']*RECEPTOR_COUNT))
    UNPACK_ALL = '>HHHHHH'

    def __init__(self, bus: SMBus, address: hex = 0x21):
        super().__init__(bus, address)
        self.receptors = [0] * self.RECEPTOR_COUNT
        self.write_reg_bytes(ReceptorRegisters.Config, self.CONFIG)

    def read_raw(self, n=None) -> List[int]:
        if n:
            if n >= self.RECEPTOR_COUNT:
                return []
            _, data = self.read_reg_bytes(self.CHANNEL[n], 2)
            data = unpack('>H', array('B', data).tostring())
        else:
            _, data = self.read_reg_bytes(self.READ_ALL, 2 * self.RECEPTOR_COUNT)
            data = list(unpack(self.UNPACK_ALL, array('B', data).tostring()))
        data = [4096 - (0x0FFF & x) for x in data]
        self.receptors = data
        return data

    def read(self, n=None) -> List[bool]:
        return [x > self.THRESHOLD for x in self.read_raw(n)]

    def __getitem__(self, item):
        if isinstance(item, slice):
            self.read()
            return self.receptors.__getitem__(item)
        elif isinstance(item, int):
            return self.read(item)
        else:
            logger.error('Bad type (not int or slice) passed to receptors.__getitem__()')
            return []


if __name__ == '__main__':
    master = SMBus(1)
    read = ReceptorControl(master)
    while True:
        print(read.read_raw())
        print(''.join(['1' if x else '0' for x in read[:]]))
        sleep(1)
