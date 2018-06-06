import smbus
from i2c.i2c_module import I2CModule

class LaserControl(I2CModule):
    LASER_COUNT=6
    _state = 0

    @property
    def state(self) -> chr:
        return self._state

    @state.setter
    def state(self, value: chr):
        self._state = value

    def __init__(self, bus, addr=0x3a):
        super().__init__(bus, addr)
        self.state = 0

    def update(self):
        # The following seems strange, and it is, but due to the incorrect construction of OUR
        # box, it is necessary to switch the last two lasers in our byte.
        posZero = (self.state & 0x10) << 1
        posOne = (self.state & 0x20) >> 1

        # Reset first two bits of state
        self.state = self.state & 0x0F
        self.state = self.state | posZero | posOne
        # Invert the 2's complement way because ~ isn't possible
        self.write_byte(-self.state - 1)

    def reset(self):
        self.state = 0x0
        self.update()

from time import sleep
def main(argv):
    bus = smbus.SMBus(1)
    lasers = LaserControl(bus)
    lasers.state = 0x0
    lasers.update()
    option = int(argv[1])
    if option == 0:
        i = 0
        while True:
            i += 1
            if i >= lasers.LASER_COUNT:
                i = 0
            lasers.state = 0x1 << i
            lasers.update()
            sleep(2)
    elif option == 1:
        lasers.state = 0x3F
        lasers.update()
    else:
        print('Huh?')

if __name__ == '__main__':
    import sys
    main(sys.argv)
