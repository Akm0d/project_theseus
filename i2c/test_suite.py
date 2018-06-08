import logging
from argparse import ArgumentParser
from time import sleep
from typing import List

from smbus2 import SMBus

from i2c.laser_i2c import LaserControl
from i2c.lid_kit import ArduinoI2C, COLOR
from i2c.lock_i2c import BoxLock
from i2c.sevenseg import SevenSeg
from i2c.switches_i2c import SwitchesI2C

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class TestSuite:
    minutes = 0
    seconds = 0
    _keypress = ""

    i2c_seven = None
    i2c_arduino = None
    i2c_lasers = None
    i2c_switches = None
    i2c_lock = None

    def __init__(self, bus: SMBus):
        try:
            self.i2c_arduino = ArduinoI2C(bus)
            logger.info("Arduino Ready")
        except OSError:
            logger.warning("Arduino setup failed")
        try:
            self.i2c_lasers = LaserControl(bus)
            logger.info("Lasers Ready")
        except OSError:
            logger.warning("Laser setup failed")

        try:
            self.i2c_seven = SevenSeg(bus).sevenseg
            logger.info("Seven Segment Display Ready")
        except OSError:
            logger.warning("Seven Segment Display setup failed")

        try:
            self.i2c_switches = SwitchesI2C(bus)
            logger.info("Switches Ready")
        except OSError:
            logger.warning("Switches setup failed")

        try:
            self.i2c_lock = BoxLock(bus)
            self.i2c_lock.close()
            logger.info("Lock ready")
        except OSError:
            logger.warning("Solenoid setup failed")

    @property
    def dots(self) -> List[bool]:
        """
        Read switches to determine the values of the dots
        """
        return self.i2c_switches.read_switches()[:4]

    @property
    def rgb(self) -> List[bool]:
        """
        Read switches to determine the value of the RGB
        """
        return self.i2c_switches.read_switches()[4:]

    @property
    def keypress(self) -> str:
        rcv = self.i2c_arduino.keypad
        for r in rcv:
            if r == '*':
                if self.i2c_lock and self.i2c_lock.powered:
                    self.i2c_lock.open()
            elif r == "#":
                """TODO Reset the timer"""
            else:
                self._keypress = r
        return self._keypress

    def run(self):
        while True:
            sleep(.1)
            self.i2c_seven(int("0x{}{}{:02}".format(self.keypress, self.minutes, self.seconds), 16), self.dots)
            rgb = self.rgb
            if not rgb[0] and not rgb[1]:
                self.i2c_arduino.color = COLOR.BLANK
            if not rgb[0] and rgb[1]:
                self.i2c_arduino.color = COLOR.RED
            if rgb[0] and not rgb[1]:
                self.i2c_arduino.color = COLOR.BLUE
            if rgb[0] and rgb[1]:
                self.i2c_arduino.color = COLOR.GREEN


if __name__ == "__main__":
    args = ArgumentParser()
    args.add_argument("--mock", action="store_true")

    opts = args.parse_args()

    TestSuite(SMBus(1)).run()

    if opts.mock:
        # Start the gui the simulates the box
        print("starting app window")
        # qt_app = Thread(target=ApplicationWindow.run)
        # qt_app.start()
        # qt_app.join()
