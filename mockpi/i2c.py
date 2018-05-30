from typing import List

from i2c.i2c_module import I2CModule
from i2c.laser_i2c import LaserControl
from i2c.receptors_i2c import ReceptorControl
from i2c.sevenseg_i2c import SevenSegDisplay


class MockReceptorControl(ReceptorControl):
    def read_all(self) -> List[bool]:
        """
        :return: True if the signal is high else false
        """
        return True

    def read(self, n) -> bool:
        return True


class MockSevenSegDisplay(SevenSegDisplay):
    def set_digits(self, digits: str):
        """
        :param digits:  A string of length 4 representing the hex characters that shouldbe ....
        :return:
        """
        if len(digits) != 4:
            return
        for i, c in enumerate(digits):
            self.chars[i] = self.CHARMAP[c]


class MockLaserControl(LaserControl):
    @property
    def state(self):
        pass

    @state.setter
    def state(self, value):
        pass


class MockI2cModule(I2CModule):
    def write_byte(self, byte):
        pass

    def write_reg_byte(self, reg, byte):
        pass

    def write_reg_bytes(self, reg, data):
        pass

    def read_byte(self):
        pass

    def read_reg_byte(self, reg):
        pass

    def read_reg_bytes(self, reg, n=32):
        pass
