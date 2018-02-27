from enum import Enum
from logging.handlers import RotatingFileHandler
from time import sleep
from multiprocessing import Lock

import logging
import random

log = logging.getLogger(__name__)
handler = RotatingFileHandler("{}.log".format(__name__), maxBytes=1280000, backupCount=1)
handler.setFormatter(logging.Formatter("[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s"))
handler.setLevel(logging.DEBUG)
log.addHandler(handler)

"""
try:
    import RPI.GPIO as GPIO
    from smbus import SMBus
except ImportError:
    log.warn("Not running on a Raspberry pi, importing Mock libraries")
    from MockPi import MockGPIO as GPIO
    from MockPi.MockSmbus import SMBus
"""


class I2C(Enum):
    """
    I2C addresses of each slave device
    """
    KNOCK_KIT = 0x01
    LED_KIT = 0x02
    LID_KIT = 0x03
    PUZZLE = 0x04
    POTENTIOMETER = 0x05


class Logic:
    _process = Lock()

    def __init__(self):
        self._bus = None
        self._i2c_master = None
        self._i2c_slave = None
        self._temp_code = None

    # TODO have a bunch of properties that change the game state and read the game state from the database

    @property
    def keypad_code(self):
        # TODO get this value from the database
        return self._temp_code

    @keypad_code.setter
    def keypad_code(self, value):
        log.debug("Setting new keypad code: 0x{}".format(value))
        # TODO put this value in the database
        self._temp_code = value

    def run(self):
        """
        Start the game and make sure there is only a single instance of this process
        This is the setup function, when it is done, it will start the game loop
        """
        with self._process:
            # Initialize I2C server
            self._bus = SMBus(0)
            # TODO Initialize all the random data, such as laser patterns and codes
            self._temp_code = '{:03x}'.format(random.randint(0, 0xfff))

            while True:
                self._loop()
                sleep(1)

    def _loop(self):
        """TODO this is the game loop that polls I2C and tracks the state of the game"""
        # Loop updates values in the database.  It is the only thing that talks to arduinos directly
        self._bus.write_byte_data(I2C.KNOCK_KIT.value, 0, 9)
        for i2c in I2C:
            # log.debug("Reading from I2C on {}".format(i2c.name))
            foo = self._bus.read_byte_data(i2c_addr=i2c.value, register=0)
            print(foo)

    def _send(self, device, cmd, message):
        """
        Send a command to a device over I2c.  Nothing external should call this, only "loop"
        :param device:
        :param cmd:
        :param message:
        :return:
        """
        log.debug("Message: " + cmd + message + " send to device " + str(device))
        self._bus.write_byte_data(i2c_addr=device, register=ord(cmd), value=bytes(message))
