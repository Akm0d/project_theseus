import logging
from argparse import ArgumentParser
from threading import Thread
from time import sleep

from smbus2 import SMBus

from i2c.laser_i2c import LaserControl
from i2c.lid_kit import ArduinoI2C, COLOR
from i2c.sevenseg import SevenSeg
from i2c.switches_i2c import SwitchesI2C

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def run_sevenseg():
    while True:
        for n in range(0xffff):
            seven.sevenseg(value=n)
            sleep(.1)


def run_rgb():
    while True:
        for c in COLOR:
            arduino.RGB(c)
            sleep(1)
        arduino.RGB(COLOR.BLANK)


def run_keypad():
    # Test Keypad
    while True:
        rcv = arduino.keypad
        if rcv:
            print(rcv)
        sleep(.1)


def run_lasers():
    while True:
        for i in range(0, 0x40):
            lasers.state = i
            lasers.update()
            sleep(.1)


def run_switches():
    old_value = 0
    while True:
        new_value = switches.read_switches()
        if old_value != new_value:
            print(new_value)
            old_value = new_value
        sleep(.01)


bus = SMBus(1)

args = ArgumentParser()
args.add_argument("--mock", action="store_true")

opts = args.parse_args()

if opts.mock:
    # Start the gui the simulates the box
    print("starting app window")
    # qt_app = Thread(target=ApplicationWindow.run)
    # qt_app.start()
    # qt_app.join()

try:
    arduino = ArduinoI2C(bus)
    Thread(target=run_rgb).start()
    Thread(target=run_keypad).start()
    logger.info("Arduino Ready")
except OSError:
    logger.warning("Arduino setup failed")

try:
    lasers = LaserControl(bus)
    Thread(target=run_lasers).start()
    logger.info("Lasers Ready")
except OSError:
    logger.warning("Laser setup failed")

try:
    seven = SevenSeg(bus)
    Thread(target=run_sevenseg).start()
    logger.info("Seven Segment Display Ready")
except OSError:
    logger.warning("Seven Segment Display setup failed")

try:
    switches = SwitchesI2C(bus)
    Thread(target=run_switches).start()
    logger.info("Switches Ready")
except OSError:
    logger.warning("Switches setup failed")
