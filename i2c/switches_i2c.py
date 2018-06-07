from bitarray import bitarray
from smbus2 import SMBus

from i2c.i2c_module import I2CModule


class SwitchesI2C(I2CModule):
    def __init__(self, bus, addr=0x3b):
        super().__init__(bus, addr)
        self.write_byte(0xff)

    @property
    def switches(self) -> int:
        _, byte = self.read_byte()
        return byte

    def read_switches(self):
        byte = bytes([self.switches])
        array = bitarray(endian='little')
        array.frombytes(byte)
        array = array[2:]
        array = array[5:6] + array[:-1]
        return [not x for x in array]


from time import sleep


if __name__ == "__main__":
    switches = SwitchesI2C(SMBus(1))
    old_val = 0
    while True:
        sleep(.01)
        val = ''.join(['1' if x else '0' for x in switches.read_switches()])
        if val != old_val:
            print(val)
            old_val = val

'''
432105
501234
'''
