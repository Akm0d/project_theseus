from time import sleep
from multiprocessing import Lock

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    import RPI.GPIO as GPIO
    import smbus
except ImportError:
    logger.warn("Not running on a Raspberry pi, importing Mock libraries")
    from MockPi import MockGPIO as GPIO, MockSmbus as smbus


class Logic:
    process = Lock()

    def __init__(self):
        # Initialize I2C server
        #self.bus = smbus.SMBus(1)
        # TODO have a bunch of properties that change the game state and read the game state from the database
        pass

    def run(self):
        """
        Start the game and make sure there is only a single instance of this process
        This is the setup function, when it is done, it will start the game loop
        """
        with self.process:
            i = 1
            while True:
                self._loop()
                print(i)
                i += 1
                sleep(1)

    def _loop(self):
        """TODO this is the game loop that polls I2C and tracks the state of the game"""
        # Loop updates values in the database.  It is the only thing that talks to arduinos directly

    def _send(self, device, cmd, message):
        """
        Send a command to a device over I2c.  Nothing external should call this, only "loop"
        :param device:
        :param cmd:
        :param message:
        :return:
        """
        logger.debug("Message: " + cmd + message + " send to device " + str(device))
        self.bus.write_byte_data(i2c_addr=device, register=ord(cmd), value=bytes(message))
