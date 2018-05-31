from bitarray import bitarray
from smbus import SMBus

from i2c.i2c_module import I2CModule


class LaserControl(I2CModule):
    LASER_COUNT = 6

    def __init__(self, bus: SMBus, address: hex = 0x3a):
        super().__init__(bus, address)
        self.lasers = None
        self._state = bitarray([False] * self.LASER_COUNT, endian='little')

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: bitarray):
        self._state = value
        self.update()

    def update(self):
        buf = bitarray(self.lasers)
        buf.invert()
        try:
            self.write_byte(buf.tobytes()[0])
        except IndexError:
            # Not actually connected to lasers
            pass

    def reset(self):
        self.lasers[:] = False
        self.update()


if __name__ == '__main__':
    from sys import argv
    from time import sleep

    master = SMBus(1)
    lasers = LaserControl(master)
    lasers.state[:] = False
    lasers.update()
    if argv[1:]:
        i = 0
        j = -1
        k = -2
        while True:
            k = j
            j = i
            i += 1
            if i >= lasers.LASER_COUNT:
                i = 0
            lasers.state[i] = True
            lasers.state[k] = False
            lasers.update()
            sleep(.1)
    else:
        lasers.state[:] = True
        lasers.update()

