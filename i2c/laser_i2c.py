from smbus2 import SMBus
from bitarray import bitarray
from i2c.i2c_module import I2CModule


class LaserControl(I2CModule):
    LASER_COUNT = 6

    def __init__(self, bus: SMBus, addr=0x3a):
        super().__init__(bus, addr)
        self._state = bitarray([False]*self.LASER_COUNT, endian='little')
        self._update()

    def __getitem__(self, pos):
        return self._state.__getitem__(pos)

    def __setitem__(self, pos, value):
        self._state.__setitem__(pos, value)
        self._update()

    def _update(self):
        buf = bitarray(self._state)
        buf.invert()
        buf[4], buf[5] = buf[5], buf[4]
        self.write_byte(buf.tobytes()[0])

    def reset(self):
        self[:] = False

from time import sleep
if __name__ == '__main__':
    from sys import argv

    master = SMBus(1)
    lasers = LaserControl(master)
    lasers[:] = False
    option = int(argv[1])
    if option == 0:
        i = 0
        j = -1
        k = -2
        while True:
            k = j
            j = i
            i += 1
            if i >= lasers.LASER_COUNT:
                i = 0
            lasers[i] = True
            lasers[k] = False

            sleep(.1)
    elif option == 1:
        lasers[:] = True
    else:
        print('Huh?')
