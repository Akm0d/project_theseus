from time import sleep
from multiprocessing import Lock

import logging
import random

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

try:
    import RPI.GPIO as GPIO
    from smbus import SMBus
except ImportError:
    log.warn("Not running on a Raspberry pi, importing Mock libraries")
    from MockPi import MockGPIO as GPIO
    from MockPi.MockSmbus import safe_import_i2c

    safe_import_i2c()
    from MockPi.MockSmbus import MockSMBus as SMBus


class Logic:
    process = Lock()

    def __init__(self):
        self._temp_code = '{:03x}'.format(random.randint(0, 0xfff))
        # Initialize I2C server
        self.bus = SMBus()
        # TODO have a bunch of properties that change the game state and read the game state from the database

    @property
    def keypad_code(self):
        # TODO get this value from the database
        return self._temp_code

    @keypad_code.setter
    def keypad_code(self, value):
        log.debug("Setting new keypad code: {}".format(value))
        # TODO put this value in the database
        self._temp_code = value

    def run(self):
        """
        Start the game and make sure there is only a single instance of this process
        This is the setup function, when it is done, it will start the game loop
        """
        with self.process:
            while True:
                self._loop()
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
        log.debug("Message: " + cmd + message + " send to device " + str(device))
        self.bus.write_byte_data(i2c_addr=device, register=ord(cmd), value=bytes(message))
