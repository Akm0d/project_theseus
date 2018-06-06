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


if __name__ == "__main__":
    banana = SwitchesI2C(SMBus(1))
    print(banana.switches)
