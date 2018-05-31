import smbus
from bitarray import bitarray
from i2c.i2c_module import I2CModule

class LaserControl(I2CModule):
    LASER_COUNT=6

    def __init__(self, bus, addr=0x3a):
        super().__init__(bus, addr)
        self.state = bitarray([False]*self.LASER_COUNT, endian='little')

    def update(self):
        buf = bitarray(self.state)
        buf.invert()
        self.write_byte(buf.tobytes()[0])

    def reset(self):
        self.lasers[:] = False
        self.update()
