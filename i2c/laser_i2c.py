from time import sleep

from bitarray import bitarray

from i2c import SMBus
from i2c.i2c_module import I2CModule


class LaserControl(I2CModule):
    LASER_COUNT = 6

    def __init__(self, bus: SMBus, address: hex = 0x3a):
        super().__init__(bus, address)
        self.lasers = None
        self.state = bitarray([False] * self.LASER_COUNT, endian='little')

    def update(self):
        buf = bitarray(self.lasers)
        buf.invert()
        self.write_byte(buf.tobytes()[0])

    def reset(self):
        self.lasers[:] = False
        self.update()


# if __name__ == '__main__':
#     from sys import argv
#
#     master = SMBus(1)
#     lasers = LaserControl(master)
#     lasers.state[:] = False
#     lasers.update()
#     option = int(argv[1])
#     if option == 0:
#         i = 0
#         j = -1
#         k = -2
#         while True:
#             k = j
#             j = i
#             i += 1
#             if i >= lasers.LASER_COUNT:
#                 i = 0
#             lasers.state[i] = True
#             lasers.state[k] = False
#             lasers.update()
#             sleep(.1)
#     elif option == 1:
#         lasers.state[:] = True
#         lasers.update()
#     else:
#         print('Huh?')
