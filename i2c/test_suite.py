import logging
from argparse import ArgumentParser
from threading import Thread
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
    DIGITS = 4
    timer_running = False
    _keypress = ["0"] * DIGITS
    dead = False
    minutes = 0
    seconds = 0

    i2c_seven = None
    i2c_arduino = None
    i2c_lasers = None
    i2c_switches = None
    i2c_lock = None

    def timer(self):
        while True:
            if self.timer_running:
                if self.seconds:
                    self.seconds -= 1
                elif self.minutes:
                    self.minutes -= 1
                    self.seconds = 59
                else:
                    self.dead = True
                    self.timer_running = False
            sleep(0.9)

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
    def keypress(self) -> List[str]:
        rcv = self.i2c_arduino.keypad
        for r in rcv:
            if r == '*':
                if self.i2c_lock and self.i2c_lock.powered:
                    self.i2c_lock.open()
            elif r == "#":
                self.timer_running = True
            else:
                self.timer_running = False
                self._keypress.append(r)
                self._keypress = self._keypress[-self.DIGITS:]
        return self._keypress

    def run_lasers(self):
        while True:
            for x in range(0x40):
                self.i2c_lasers.state = x
                sleep(0.3)

    def run(self):
        Thread(target=self.timer).start()
        Thread(target=self.run_lasers).start()

        while True:
            sleep(.1)
            self.i2c_seven(int("0x{}".format(
                "".join(self.keypress) if not self.timer_running else "{}{:02}".format(self.minutes, self.seconds)), 16)
                , self.dots)
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
