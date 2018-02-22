from time import sleep
from threading import Lock

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    import RPI.GPIO as GPIO
    import smbus
    import spi
except ImportError:
    logger.warn("Not running on Raspberry pi, importing Mock libraries")
    # TODO Import mock libraries
    # https: // github.com / adafruit / Adafruit_Python_GPIO / tree / master / tests


class Logic:
    process = Lock()

    def __init__(self):
        # Initialize I2C server
        self.bus = smbus.SMBus(1)
        # TODO have a bunch of properties that change the game state and read the game state from the database

    def run(self):
        """Start the game and make sure there is only a single instance of this process"""
        with self.process:
            while True:
                self.loop()
                sleep(1)

    def loop(self):
        """TODO this is the game loop that polls I2C and tracks the state of the game"""
        # Loop updates values in the database.  It is the only thing that talks to arduinos directly

    def _send(self, device, cmd, message):
        """
        Send a command to a device over I2c
        :param device:
        :param cmd:
        :param message:
        :return:
        """
        logger.debug("Message: " + cmd + message + " send to device " + str(device))
        self.bus.write_byte_data(i2c_addr=device, register=ord(cmd), value=bytes(message))
