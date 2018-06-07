from enum import IntEnum

from smbus2 import SMBus

from i2c.i2c_module import I2CModule


class COLOR(IntEnum):
    BLANK = 0b0000000
    RED = 0b11100000
    GREEN = 0b00011100
    BLUE = 0b0000011


class ArduinoI2C(I2CModule):
    ADDRESS = 0x0d
    NO_DATA = '.'.encode()
    EMPTY = b'\xff'

    def __init__(self, bus: SMBus, address: hex = 0x69):
        I2CModule.__init__(self, bus, address)
        self.current_color = COLOR.BLANK

    def RGB(self, color: COLOR):
        self.current_color = color
        self.write_byte(color)

    @property
    def keypad(self) -> chr:
        # TODO device won't read data unless listening on serial too
        # success, data = self.read_reg_bytes(self.current_color, 16)
        success, data = self.read_bytes(16)
        data = [chr(x) for x in data if x.to_bytes(1, 'little') != self.NO_DATA and x.to_bytes(1, 'little') != self.EMPTY]
        return data


if __name__ == "__main__":
    from time import sleep

    device = ArduinoI2C(SMBus(1))

    # Test RGB
    for c in COLOR:
        device.RGB(c)
        sleep(.25)
    device.RGB(COLOR.BLANK)

    # Test Keypad
    while True:
        sleep(.25)
        rcv = device.keypad
        if rcv:
            print(rcv)
