import logging
import random
from datetime import time
from multiprocessing import Lock

from smbus import SMBus

<<<<<<< Updated upstream
from MockPi.MockSmbus import MockBus
from game.constants import I2C, STATE, RGBColor, COMMUNICATION, SOLENOID_STATE, ULTRASONIC_STATE, TIME_GIVEN
=======
from game.constants import I2C, STATE, TIME_GIVEN, SLEEP_INTERVAL, INTERRUPTS_PER_SECOND, TIME_OVER, RGBColor, MAX_TIME, \
    COMMUNICATION, LOGGING_LEVEL, SOLENOID_STATE, ULTRASONIC_STATE
>>>>>>> Stashed changes
from game.database import Database, Row

log = logging.getLogger(__name__)


class Logic:
    mock = True
    _comQueue = None
    _counter = 0
    _process = Lock()
    _state = STATE.WAIT
    _solenoid = SOLENOID_STATE.UNLOCKED
    _ultrasonic = ULTRASONIC_STATE.ENABLED

    def __init__(self):
        self.db = Database()
        self._bus = None
        self._counter = 0
        self._timer = 0
        self._i2c_master = None
        self._i2c_slave = None

        self._start_time = time()

    @property
    def ultrasonic(self):
        return self._ultrasonic

    @ultrasonic.setter
    def ultrasonic(self, value: ULTRASONIC_STATE):
        self._ultrasonic = value

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
    def lasers(self) -> bin:
        return self.db.last.lasers

    @lasers.setter
    def lasers(self, value: int):
        assert 0 <= value < 128
        log.debug("Setting new laser configuration: {}".format(bin(value)))
        # TODO Send the command over i2c to activate the correct lasers
        self.db.last = Row(lasers=value)

    @property
    def keypad_code(self) -> hex:
        return self.db.last.code

    @keypad_code.setter
    def keypad_code(self, value: hex):
        try:
            typed = int(value)
        except ValueError:
            typed = int("0x" + str(value), 16)
        assert 0x0 <= typed <= 0xfff
        log.debug("Setting new keypad code: 0x{}".format(typed))
        self.db.last = Row(code=typed)

    @property
    def team(self) -> str:
        return self.db.last.name

    @team.setter
    def team(self, value: str):
        log.debug("Setting current team name to: {}".format(value))
        self.db.last = Row(name=value)

    @property
    def rgb_color(self) -> RGBColor:
        return RGBColor(self.db.last.color)

    @rgb_color.setter
    def rgb_color(self, value: RGBColor):
        log.debug("Setting new rgb color: {}".format(value))
        # TODO send the command over i2c to change the rgb color
        self.db.last = Row(color=value.value)

    def run(self, queue, mock: bool = False):
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

            self.state = STATE.WAIT  # Change state of game to WAIT
            self.solenoid = SOLENOID_STATE.LOCKED
            self.comQueue = queue
            self.ultrasonic = ULTRASONIC_STATE.ENABLED

            try:
                while True:
                    self._loop()
                    # sleep(SLEEP_INTERVAL)
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
        elif command_id is COMMUNICATION.GET_ULTRASONIC:
            command_id = None
            self.comQueue.put([COMMUNICATION.SENT_ULTRASONIC, self.ultrasonic])
        elif command_id is COMMUNICATION.TOGGLE_ULTRASONIC:
            command_id = None
            if self.ultrasonic is ULTRASONIC_STATE.ENABLED:
                self.ultrasonic = ULTRASONIC_STATE.DISABLED
            else:
                self.ultrasonic = ULTRASONIC_STATE.ENABLED
            self.comQueue.put([COMMUNICATION.SENT_ULTRASONIC, self.ultrasonic])
            # No return message is necessary

        # State Actions
        if self.state is STATE.WAIT:
            pass
        elif self.state is STATE.RUNNING:
            pass
        elif self.state is STATE.EXPLODE:
            pass
            # TODO randomize laser pattern so that they flash
        elif self.state is STATE.WIN:
            pass
        else:
            log.error("Reached an unknown state: {}".format(self.state))

        # State Transitions
        if self.state is STATE.WAIT:
            if command_id is COMMUNICATION.START_GAME:
                command_id = None
                self.state = STATE.RUNNING
                self.start_game()
        elif self.state is STATE.RUNNING:
            if command_id is COMMUNICATION.RESET_GAME:
                command_id = None
                self.state = STATE.WAIT
            elif command_id is COMMUNICATION.KILL_PLAYER:
                command_id = None
                self.state = STATE.EXPLODE
                self.db.last.success = False
            elif command_id is COMMUNICATION.DEFUSED:
                command_id = None
                self.state = STATE.WIN
                self.db.last.success = True
        elif self.state is STATE.EXPLODE:
            if command_id is COMMUNICATION.RESET_GAME:
                command_id = None
                self.state = STATE.WAIT
                # Lock solenoid
                self.solenoid = SOLENOID_STATE.LOCKED
                self.comQueue.put([COMMUNICATION.SENT_SOLENOID_STATUS, self.solenoid])
        elif self.state is STATE.WIN:
            if command_id is COMMUNICATION.RESET_GAME:
                command_id = None
                self.state = STATE.WAIT
                # Lock solenoid
                self.solenoid = SOLENOID_STATE.LOCKED
                self.comQueue.put([COMMUNICATION.SENT_SOLENOID_STATUS, self.solenoid])
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

    @staticmethod
    def random_laser_pattern()-> int:
        # TODO make sure the laser pattern conforms to certain rules
        return random.randint(0, 127)

    def start_game(self):
        """
        Add a row to the database, generate random data for all the puzzles
        """
        row = Row(
            name=self.db.last.name, lasers=self.random_laser_pattern(), code=random.randint(0, 0xfff), success=False,
            color=random.choice([RGBColor.RED.value, RGBColor.BLUE.value]), time=TIME_GIVEN
        )

        log.debug("Adding new row to the database:\n{}".format(row))
        self.db.add_row(row)

