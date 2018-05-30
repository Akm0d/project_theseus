try:
    import RPi.GPIO as GPIO
    from smbus import SMBus
    from sys import argv

    if "--mock" in argv:
        raise ImportError
    from os import path
    if not path.exists("/dev/i2c-1"):
        raise ImportError
except ImportError:
    print("Importing Mock libraries")
    from MockPi.MockSmbus import MockBus as SMBus
    from MockPi.MockGPIO import MockGPIO as GPIO
