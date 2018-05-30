try:
    import RPi.GPIO as GPIO
    from smbus import SMBus
    from sys import argv

    if "--mock" in argv:
        raise ModuleNotFoundError
    from os import path
    if not path.exists("/dev/i2c-1"):
        raise ModuleNotFoundError
except ModuleNotFoundError or ImportError:
    print("Importing MockSMBus library")
    from MockPi.MockSmbus import MockBus as SMBus
