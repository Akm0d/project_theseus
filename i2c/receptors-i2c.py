import struct
from array import array
from time import sleep

import smbus
from i2c.i2c_module import I2CModule


class ReceptorControl(I2CModule):
    RECEPTOR_COUNT = 6
    REG = {
        'Conversion': 0x00,
        'Alert': 0x01,
        'Config': 0x02,
        'CycleTime': 0x03,
        'Data1Low': 0x04,
        'Data1High': 0x05,
        'Hyst1': 0x06,
        'Data2Low': 0x07,
        'Data2High': 0x08,
        'Hyst2': 0x09,
        'Data3Low': 0x0A,
        'Data3High': 0x0B,
        'Hyst3': 0x0C,
        'Data4Low': 0x0D,
        'Data4High': 0x0E,
        'Hyst4': 0x0F
    }
    CHANNEL = [0x80, 0x90, 0xA0, 0xB0, 0xC0, 0xD0, 0xE0, 0xF0]
    CONFIG = [0x03, 0xF8]
    READ_ALL = 0x70
    # UNPACK_ALL = ''.join(['>'].extend(['H']*RECEPTOR_COUNT))
    UNPACK_ALL = '>HHHHHH'

    def __init__(self, bus, addr=0x21):
        super().__init__(bus, addr)
        self.receptors = [0] * self.RECEPTOR_COUNT
        self.write_reg_bytes(self.REG['Config'], self.CONFIG)

    def read_all(self):
        _, data = self.read_reg_bytes(self.READ_ALL, 2 * self.RECEPTOR_COUNT)
        self.receptors = list(struct.unpack(self.UNPACK_ALL, array('B', data).tostring()))
        return self.receptors

    def read(self, n):
        sleep(.5)
        if n >= self.RECEPTOR_COUNT:
            return None
        _, data = self.read_reg_bytes(self.CHANNEL[n], 2)
        data2 = struct.unpack('>H', array('B', data).tostring())
        self.receptors[n] = data2[0]
        return self.receptors[n]


if __name__ == '__main__':
    bus = smbus.SMBus(1)
    read = ReceptorControl(bus)
    while True:
        # print('{}, {}, {}, {}, {}, {}'.format(*[read.read(n) for n in range(6)]))
        # print(read.read_all())
        print(read.read(1))
        sleep(1)
