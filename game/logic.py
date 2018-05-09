from datetime import time
from logging.handlers import RotatingFileHandler
from multiprocessing import Lock
from MockPi.MockSmbus import MockBus
from smbus import SMBus
from time import sleep

import logging
import random

from game.constants import I2C, STATE, TIME_GIVEN, SLEEP_INTERVAL, INTERRUPTS_PER_SECOND, TIME_OVER, RGBColor, MAX_TIME, COMMUNICATION, LOGGING_LEVEL, SOLENOID_STATE
from game.database import Database, Row

import datetime

log = logging.getLogger(__name__)
handler = RotatingFileHandler("{}.log".format(__name__), maxBytes=1280000, backupCount=1)
handler.setFormatter(logging.Formatter("[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s"))
handler.setLevel(LOGGING_LEVEL)
log.addHandler(handler)


class Logic:
    STATE_FILE = ".state"
    _code = "000"
    _comQueue = None
    _counter = 0
    _mock = False
    _process = Lock()
    _state = STATE.WAIT
    _timer = TIME_GIVEN
    _solenoid = SOLENOID_STATE.UNLOCKED

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def comQueue(self):
        return self._comQueue

    @comQueue.setter
    def comQueue(self, value):
        log.debug("Queue was created")
        self._comQueue = value

    @property
    def counter(self):
        return self._counter

    @counter.setter
    def counter(self, value: int):
        self._counter = value

    @property
    def solenoid(self):
        return self._solenoid

    @solenoid.setter
    def solenoid(self, value: SOLENOID_STATE):
        self._solenoid = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: STATE):
        log.debug("State changed from {} to {}".format(self._state.value, value.value))
        self._state = value

    @property
    def timer(self):
        return self._timer

    @timer.setter
    def timer(self, value):
        log.debug("Timer set to {}".format(value))
        self._timer = value

    @property
    def mock(self):
        return self._mock

    @mock.setter
    def mock(self, value: bool):
        log.debug("mock was set to {}".format(value))
        self._mock = value

    def __init__(self):
        self.db = Database()
        self._bus = None
        self._counter = 0
        self._i2c_master = None
        self._i2c_slave = None

        # Sensor states
        self._lasers = None
        self._rgb_color = None

        # Software states
        self._team = "--"
        self._code = 0x123
        self._time = MAX_TIME

        self._start_time = time()

    @property
    def time(self) -> str:
        """
        Return the string value that should be displayed on the timer
        :return: The number of minutes and seconds remaining in this attempt I.E '03:12'
        """
        minutes = int(self._time / 60)
        seconds = self._time - (minutes * 60)
        if self.state is STATE.EXPLODE:
            return "BOOM!"
        elif self.state is STATE.WIN:
            return "SUCCESS!"
        else:
            return "{:02}:{:02}".format(minutes, seconds)

    @time.setter
    def time(self, value: int):
        self._time = value

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
    def team(self) -> str:
        return self._team

    @team.setter
    def team(self, value: str):
        log.debug("Setting current team name to: {}".format(value))
        self.db.last = Row(name=value)
        self._team = value

    @property
    def rgb_color(self) -> RGBColor:
        return self._rgb_color

    @rgb_color.setter
    def rgb_color(self, value: RGBColor):
        log.debug("Setting new rgb color: {}".format(value))
        # TODO send the command over i2c to change the rgb color
        if value in [RGBColor.BLUE, RGBColor.RED]:
            self.db.last = Row(color=value.value)
        self._rgb_color = value

    def run(self, queue, mock: bool = False, debug: bool = False, logLevel: int = 0):
        """
        Start the game and make sure there is only a single instance of this process
        This is the setup function, when it is done, it will start the game loop
        """
        with self._process:
            # Initialize I2C server
            if mock:
                self._bus = MockBus(1)
                self.mock = True
            else:
                self._bus = SMBus(1)
                self.mock = False

            # Initialize all the random data, such as laser patterns and codes
            self.keypad_code = '{:03x}'.format(random.randint(0, 0xfff))
            self.lasers = random.randint(1, 0x3f)
            self.state = STATE.WAIT  # Change state of game to WAIT
            self.timer = TIME_GIVEN
            self.team = "--"
            self.solenoid = SOLENOID_STATE.UNLOCKED
            self.comQueue = queue
            self.code = "000"

            try:
                while True:
                    self._loop()
                    sleep(SLEEP_INTERVAL)
            except KeyboardInterrupt:
                return

    def poll_sensors(self):
        """
        Poll all of the sensors and rais a flag if one of them has tripped
        """
        # self._bus.write_byte_data(I2C.LASERS.value, 0, 9) # for i2c in I2C:
        #     log.debug("Reading from I2C on {}".format(i2c.name))
        #     foo = self._bus.read_word_data(i2c.value, 0)
        #     self._send(I2C.SEVEN_SEG, "Hello!")
        pass

    def _loop(self):
        command = None
        command_id = None
        if not self.comQueue.empty():
            command = self.comQueue.get()
            command_id = command[0]

        # State independent actions
        if command_id is COMMUNICATION.GET_STATE:
            command_id = None
            self.comQueue.put([COMMUNICATION.SENT_STATE, self.state])
        elif command_id is COMMUNICATION.SOLENOID_STATUS:
            command_id = None
            self.comQueue.put([COMMUNICATION.SENT_SOLENOID_STATUS, self.solenoid])
        elif command_id is COMMUNICATION.TOGGLE_SOLENOID:
            command_id = None
            if self.solenoid is SOLENOID_STATE.UNLOCKED:
                self.solenoid = SOLENOID_STATE.LOCKED
            else:
                self.solenoid = SOLENOID_STATE.UNLOCKED
            self.comQueue.put([COMMUNICATION.SENT_SOLENOID_STATUS, self.solenoid])
        elif command_id is COMMUNICATION.GET_CODE:
            command_id = None
            self.comQueue.put([COMMUNICATION.SENT_CODE, self.code])
        elif command_id is COMMUNICATION.SET_CODE:
            command_id = None
            self.code = command[1]
            # No return message is necessary


        # State Actions
        if self.state is STATE.WAIT:
            self.time = MAX_TIME
            if command_id is COMMUNICATION.GET_TIMER:
                command_id = None
                self.comQueue.put([COMMUNICATION.TIMER_TEXT, datetime.datetime.strftime(self.timer, "%M:%S")])
        elif self.state is STATE.RUNNING:
            if self.counter < INTERRUPTS_PER_SECOND:
                self.counter = self.counter + 1
            else:
                self.counter = 0
                # Decrement time
                self.timer = self.timer - datetime.timedelta(seconds=1)
            if command_id is COMMUNICATION.GET_TIMER:
                command_id = None
                # Show the current time
                self.comQueue.put([COMMUNICATION.TIMER_TEXT, datetime.datetime.strftime(self.timer, "%M:%S")])
        elif self.state is STATE.EXPLODE:
            if command_id is COMMUNICATION.GET_TIMER:
                command_id = None
                self.comQueue.put([COMMUNICATION.TIMER_TEXT, "DEAD"])
                # TODO randomize laser pattern so that they flash
        elif self.state is STATE.WIN:
            if command_id is COMMUNICATION.GET_TIMER:
                command_id = None
                self.comQueue.put([COMMUNICATION.TIMER_TEXT, "SUCCESS!"])
        else:
            log.error("Reached an unknown state: {}".format(self.state))

        # State Transitions
        if self.state is STATE.WAIT:
            if command_id in [COMMUNICATION.START_GAME, COMMUNICATION.TOGGLE_TIMER]:
                command_id = None
                self.state = STATE.RUNNING
                # Reset timer
                self.timer = TIME_GIVEN
        elif self.state is STATE.RUNNING:
            if command_id is COMMUNICATION.TOGGLE_TIMER:
                command_id = None
                # Reset timer
                self.timer = TIME_GIVEN
                self.state = STATE.WAIT
        elif self.state is STATE.EXPLODE:
            if command_id is COMMUNICATION.TOGGLE_TIMER:
                command_id = None
                # Reset timer
                self.timer = TIME_GIVEN
                self.state = STATE.WAIT
        elif self.state is STATE.WIN:
            if command_id is COMMUNICATION.TOGGLE_TIMER:
                command_id = None
                # Reset timer
                self.timer = TIME_GIVEN
                self.state = STATE.WAIT

        if command_id is not None:
            # If the command wasn't used, it is for the other process, put it back
            self.comQueue.put(command)

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