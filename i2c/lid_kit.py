from i2c import SMBus


class ArduinoI2C:
    ADDRESS = 0x69

    def __init__(self, bus: SMBus):
        self.bus = bus

    def RGB(self):
        for i in range(0xffff):
            data = self.bus.read_byte_data(self.ADDRESS, i)
            if data > 0:
                print(data)
                print(chr(data))

    @property
    def keypad(self) -> hex:
        val = self.bus.read_i2c_block_data(0x70, 0, 32)
        print("".join(chr(x) for x in val))
        print(str(val))

        byte = self.bus.read_byte(0x70)
        print(byte)
        print(chr(byte))

        # "." [63, 63, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        return 0


if __name__ == "__main__":
    pass
