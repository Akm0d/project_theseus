# try:
from smbus2 import SMBusWrapper as SMBus
from sys import argv

if "--mock" in argv:
    raise ImportError
from os import path

if not path.exists("/dev/i2c-1"):
    raise ImportError
# except ImportError:
#    print("Importing Mock libraries")
#    from mockpi.smbus import MockBus as SMBus
#    from mockpi.gpio import MockGPIO as GPIO
#    from mockpi.i2c import MockI2cModule, MockLaserControl, MockReceptorControl, MockSevenSegDisplay
