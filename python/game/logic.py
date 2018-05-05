from logging.handlers import RotatingFileHandler
from multiprocessing import Lock
from MockPi.MockSmbus import MockBus
from smbus import SMBus
from time import sleep

import logging
import random

from game.constants import I2C, STATE
from game.database import Database, Row

log = logging.getLogger(__name__)
handler = RotatingFileHandler("{}.log".format(__name__), maxBytes=1280000, backupCount=1)
handler.setFormatter(logging.Formatter("[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s"))
handler.setLevel(logging.DEBUG)
log.addHandler(handler)


class Logic:
    _process = Lock()

    _state = STATE.WAIT

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: STATE):
        log.debug("State changed from {} to {}".format(self._state.value, value.value))
        self._state = value

    def __init__(self):
        self.db = Database()
        self._bus = None
        self._i2c_master = None
        self._i2c_slave = None

        # Sensor states
        self._code = None
        self._lasers = None
        self._rgb_color = None

    @property
    def lasers(self) -> bin:
        return self._lasers

    @lasers.setter
    def lasers(self, value: int):
        # TODO make sure the value is acceptable beofore applying it
        log.debug("Setting new laser configuration: {}".format(bin(value)))
        # TODO Send the command over i2c to activate the correct lasers
        self.db.last = Row(lasers=value)
        self._code = value

    @property
    def keypad_code(self) -> hex:
        return self._code

    @keypad_code.setter
    def keypad_code(self, value: hex):
        # TODO make sure the value is acceptable beofore applying it
        log.debug("Setting new keypad code: 0x{}".format(value))
        self.db.last = Row(code=value)
        self._code = value

    @property
    def rgb_color(self) -> str:
        return self._rgb_color

    @rgb_color.setter
    def rgb_color(self, value: str):
        # TODO make sure the value is acceptable beofore applying it
        log.debug("Setting new rgb color: {}".format(value))
        # TODO send the command over i2c to change the rgb color
        self.db.last = Row(color=value)
        self._rgb_color = value

    def run(self, mock: bool=False):
        """
        Start the game and make sure there is only a single instance of this process
        This is the setup function, when it is done, it will start the game loop
        """
        with self._process:
            # Initialize I2C server
            if mock:
                self._bus = MockBus(1)
            else:
                self._bus = SMBus(1)
            # Initialize all the random data, such as laser patterns and codes
            self.keypad_code = '{:03x}'.format(random.randint(0, 0xfff))
            self.lasers = random.randint(1, 0x3f)
            self.rgb_color = random.choice(["red", "blue"])

            try:
                while True:
                    self._loop()
                    sleep(1)
            except KeyboardInterrupt:
                return

    def _loop(self):
        """TODO this is the game loop that polls I2C and tracks the state of the game"""
        # Loop updates values in the database.  It is the only thing that talks to arduinos directly
        # self._bus.write_byte_data(I2C.LASERS.value, 0, 9)
        # for i2c in I2C:
        #     log.debug("Reading from I2C on {}".format(i2c.name))
        #     foo = self._bus.read_word_data(i2c.value, 0)
        #     self._send(I2C.SEVEN_SEG, "Hello!")
        if self.state is STATE.WAIT:
            pass
        elif self.state is STATE.RUNNING:
            pass
        elif self.state is STATE.EXPLODE:
            pass
        elif self.state is STATE.WIN:
            pass
        else:
            log.error("Reached an unknown state: {}".format(self.state))

    def _send(self, device: I2C, message: str):
        """
        Send a command to a device over I2c.  Nothing external should call this, only "loop"
        :param device:
        :param message:
        :return:
        """
        assert len(message) < 32
        log.debug("Address: 0x{:02x}  Message: '{}'".format(device.value, message))
        try:
            self._bus.write_i2c_block_data(device.value, 0x00, [ord(c) for c in message])
        except IOError:
            pass
