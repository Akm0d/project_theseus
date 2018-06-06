from threading import Thread
from time import sleep

from smbus2 import SMBus

from i2c.laser_i2c import LaserControl
from i2c.lid_kit import ArduinoI2C, COLOR
from i2c.sevenseg import SevenSeg

bus = SMBus(1)

arduino = ArduinoI2C(bus)
lasers = LaserControl(bus)
seven = SevenSeg(bus)


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


def run_lasers():
    while True:
        for i in range(0, 0x40):
            lasers.state = i
            lasers.update()
            sleep(.1)


if __name__ == "__main__":
    from argparse import ArgumentParser

    args = ArgumentParser()
    args.add_argument("--mock", action="store_true")

    opts = args.parse_args()
    print("starting sevenseg")
    Thread(target=run_sevenseg).start()
    print("starting rgb")
    # Thread(target=run_rgb).start()
    print("starting keypad")
    # Thread(target=run_keypad).start()
    print("starting lasers")
    Thread(target=run_lasers).start()

    if opts.mock:
        # Start the gui the simulates the box
        print("starting app window")
        # qt_app = Thread(target=ApplicationWindow.run)
        # qt_app.start()
        # qt_app.join()
