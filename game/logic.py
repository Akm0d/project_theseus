import logging
import random
from datetime import datetime
from multiprocessing import Lock, Manager, Queue
from time import sleep

from smbus import SMBus

from MockPi.MockSmbus import MockBus
from game.constants import I2C, STATE, RGBColor, INTERRUPT, SOLENOID_STATE, ULTRASONIC_STATE, MAX_TIME, SLEEP_INTERVAL
from game.database import Database, Row
from globals import ComQueue

log = logging.getLogger(__name__)


class Logic:
    db = Database()
    shared = Manager().dict()
    mock = True
    _comQueue = Queue()
    _process = Lock()
    _solenoid = SOLENOID_STATE.UNLOCKED
    _ultrasonic = ULTRASONIC_STATE.ENABLED

    def __init__(self):
        self._bus = None
        self._timer = 0
        self._i2c_master = None
        self._i2c_slave = None

    @property
    def timer_text(self) -> str:
        newDatetime = datetime.now() - self.start_time
        seconds = MAX_TIME - newDatetime.seconds
        minutes = seconds // 60
        secondsToPrint = seconds - minutes * 60
        if self.state is STATE.WAIT:
            return "RESET"
        if self.state is STATE.RUNNING:
            if minutes < 0 or seconds < 0:
                ComQueue().getComQueue().put([INTERRUPT.KILL_PLAYER])
                return "DEAD"
        elif self.state is STATE.EXPLODE:
            return "DEAD"
        elif self.state is STATE.WIN:
            return "SUCCESS!"
        return "{}:{:2}".format(minutes, secondsToPrint)

    @property
    def start_time(self) -> datetime:
        return self.shared.get("start time", datetime.now())

    @start_time.setter
    def start_time(self, value: datetime):
        self.shared["start time"] = value

    @property
    def ultrasonic(self) -> ULTRASONIC_STATE:
        return ULTRASONIC_STATE(self.shared.get("ultrasonic", ULTRASONIC_STATE.ENABLED.value))

    @ultrasonic.setter
    def ultrasonic(self, value: ULTRASONIC_STATE):
        # TODO send the new ultrasonic logic over I2C
        log.debug("Ultrasonic logic changed from {} to {}".format(self.ultrasonic.value, value.value))
        self.shared["ultrasonic"] = value.value

    @property
    def comQueue(self) -> Queue:
        return self._comQueue

    @comQueue.setter
    def comQueue(self, value):
        log.debug("Queue was created")
        self._comQueue = value

    @property
    def solenoid(self) -> SOLENOID_STATE:
        return SOLENOID_STATE(self.shared.get("solenoid", SOLENOID_STATE.UNLOCKED.value))

    @solenoid.setter
    def solenoid(self, value: SOLENOID_STATE):
        # TODO send the new solenoid logic over I2C
        log.debug("Solenoid logic changed from {} to {}".format(self.solenoid.value, value.value))
        self.shared["solenoid"] = value.value

    @property
    def state(self):
        return STATE(self.shared.get("logic", STATE.WAIT.value))

    @state.setter
    def state(self, value: STATE):
        log.debug("State changed from {} to {}".format(self.state.value, value.value))
        self.shared["logic"] = value.value

    @property
    def lasers(self) -> bin:
        return self.shared.get("lasers", 0x00)

    @lasers.setter
    def lasers(self, value: int):
        assert 0 <= value < 128
        log.debug("Setting new laser configuration: {}".format(bin(value)))
        # TODO Send the command over i2c to activate the correct lasers
        self.shared["lasers"] = value

    @property
    def keypad_code(self) -> hex:
        return self.shared.get("code", random.randint(0, 0xfff))

    @keypad_code.setter
    def keypad_code(self, value: hex):
        assert 0x0 <= value <= 0xfff
        log.debug("Setting new keypad code: 0x{}".format(value))
        self.shared["code"] = value

    @property
    def team(self) -> str:
        return self.shared.get("team", self.db.last.name)

    @team.setter
    def team(self, value: str):
        log.debug("Setting current team name to: {}".format(value))
        self.shared["team"] = value
        if (self.state is STATE.EXPLODE) or (self.state is STATE.WIN):
            self.db.last = Row(name=value)

    @property
    def rgb_color(self) -> RGBColor:
        return RGBColor(self.shared.get("rgb", RGBColor.BLANK.value))

    @rgb_color.setter
    def rgb_color(self, value: RGBColor):
        log.debug("Setting new rgb color: {}".format(value))
        # TODO send the command over i2c to change the rgb color
        self.shared["rgb"] = value.value

    def run(self, queue: Queue, mock: bool = False):
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

            self.state = STATE.WAIT  # Change logic of game to WAIT
            self.solenoid = SOLENOID_STATE.LOCKED
            self.comQueue = queue
            self.ultrasonic = ULTRASONIC_STATE.ENABLED

            try:
                while True:
                    self._loop()
                    sleep(SLEEP_INTERVAL)
            except KeyboardInterrupt:
                return

    def poll_sensors(self):
        """
        Poll all of the sensors and raise a flag if one of them has tripped
        """
        # self._bus.write_byte_data(I2C.LASERS.value, 0, 9) # for i2c in I2C:
        #     log.debug("Reading from I2C on {}".format(i2c.name))
        #     foo = self._bus.read_word_data(i2c.value, 0)
        #     self._send(I2C.SEVEN_SEG, "Hello!")
        pass

    def _loop(self):
        command_id = None
        if not self.comQueue.empty():
            command = self.comQueue.get()
            command_id = command[0]

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
            if command_id is INTERRUPT.TOGGLE_TIMER:
                self.state = STATE.RUNNING
                self.start_game()
        elif self.state is STATE.RUNNING:
            if command_id is INTERRUPT.RESET_GAME or command_id is INTERRUPT.TOGGLE_TIMER:
                self.state = STATE.WAIT
            elif command_id is INTERRUPT.KILL_PLAYER:
                self.state = STATE.EXPLODE
                self.end_game(success=False)
            elif command_id is INTERRUPT.DEFUSED:
                self.state = STATE.WIN
                self.end_game(success=True)
        elif self.state is STATE.EXPLODE:
            if command_id is INTERRUPT.RESET_GAME or command_id is INTERRUPT.TOGGLE_TIMER:
                self.state = STATE.WAIT
        elif self.state is STATE.WIN:
            if command_id is INTERRUPT.RESET_GAME or command_id is INTERRUPT.TOGGLE_TIMER:
                self.state = STATE.WAIT

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
    def random_laser_pattern() -> int:
        # TODO make sure the laser pattern conforms to certain rules
        return random.randint(0, 127)

    def start_game(self):
        """
        Add a row to the database, generate random data for all the puzzles
        """
        self.solenoid = SOLENOID_STATE.LOCKED
        self.start_time = datetime.now()
        self.lasers = self.random_laser_pattern()
        self.keypad_code = random.randint(0, 0xfff)
        self.rgb_color = random.choice([RGBColor.RED, RGBColor.BLUE])
        row = Row(
            name=self.team, lasers=self.lasers, code=self.keypad_code, success=False, time=MAX_TIME,
            color=self.rgb_color.value,
        )
        log.debug("Adding new row to the database:\n{}".format(row))
        self.db.add_row(row)

    def end_game(self, success: bool = False):
        log.debug("Game Over")
        self.db.last = Row(
            code=self.keypad_code,
            lasers=self.lasers,
            success=success,
            time=(datetime.now() - self.start_time).seconds
        )
