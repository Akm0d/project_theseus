from enum import IntEnum

from i2c import SMBus


class COLOR(IntEnum):
    BLANK = 0b0000000
    RED = 0b11100000
    GREEN = 0b00011100
    BLUE = 0b0000011


class ArduinoI2C:
    ADDRESS = 0x69
    NO_DATA = "."

    def __init__(self, bus: SMBus):
        self.bus = bus

    def RGB(self, color: COLOR):
        self.bus.write_byte(self.ADDRESS, color)

    @property
    def keypad(self) -> chr:
        # TODO device won't read data unless listening on serial too
        byte = self.bus.read_byte(self.ADDRESS)
        if byte > 0:
            key = chr(byte)
            if key is not self.NO_DATA:
                return key


if __name__ == "__main__":
    from time import sleep

    device = ArduinoI2C(SMBus(1))

    # Test RGB
    for c in COLOR:
        device.RGB(c)
        sleep(1)
    device.RGB(COLOR.BLANK)

    # Test Keypad
    while True:
        rcv = device.keypad
        if rcv:
            print(rcv)
