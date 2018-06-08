import logging
import random
from datetime import datetime
from multiprocessing import Lock, Manager, Queue
from typing import Tuple

from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
from flask_apscheduler import APScheduler
from smbus2 import SMBus

from game.constants import I2C, STATE, RGBColor, INTERRUPT, SOLENOID_STATE, ULTRASONIC_STATE, MAX_TIME, LaserPattern, \
    SECONDS_PER_PATTERN, LaserPatternValues
from game.database import Database, Row
from globals import ComQueue
from i2c.laser_i2c import LaserControl
from i2c.lid_kit import ArduinoI2C
from i2c.receptors_i2c import ReceptorControl
from i2c.sevenseg import SevenSeg
from i2c.lock_i2c import BoxLock

log = logging.getLogger(__name__)


class Logic:
    bus_num = 1
    db = Database()
    shared = Manager().dict()
    scheduler = None
    lasers = None
    _comQueue = Queue()
    _process = Lock()
    _solenoid = SOLENOID_STATE.UNLOCKED
    _ultrasonic = ULTRASONIC_STATE.ENABLED
    _laserState = LaserPattern.LASER_OFF
    _laserCounter = 0
    _patternIndex = 0
    _laserValue = 0x00

    def __init__(self):
        self.laserPattern = LaserPattern.ONE_CYCLES
        self._timer = 0
        self._patternIndex = 0

        # Initialize ICc Devices
        self._bus = SMBus(self.bus_num)
        self.lasers = LaserControl(self._bus, I2C.LASERS)
        self.sevenseg = SevenSeg(self._bus, I2C.SEVENSEG).sevenseg
        self.arduino = ArduinoI2C(self._bus, I2C.ARDUINO)
        self.photo_resistors = ReceptorControl(self._bus, I2C.PHOTO_RESISTORS)
        self.lock = BoxLock(self._bus, I2C.SOLENOID)


    @property
    def patternIndex(self) -> int:
        return self._patternIndex

    @patternIndex.setter
    def patternIndex(self, value: int):
        self._patternIndex = value

    @property
    def laserCounter(self) -> int:
        return self._laserCounter

    @laserCounter.setter
    def laserCounter(self, value: int):
        self._laserCounter = value

    def laserCounterIncrement(self):
        self.laserCounter = self.laserCounter + 1

    @property
    def laserState(self) -> LaserPattern:
        return LaserPattern(self.shared.get("laserpattern", LaserPattern.LASER_OFF.value))

    @laserState.setter
    def laserState(self, value: LaserPattern):
        self.shared["laserpattern"] = value.value

    @property
    def laserValue(self) -> int:
        return self.shared.get("laservalue", 0x00)

    @laserValue.setter
    def laserValue(self, value: int):
        self.shared["laservalue"] = value

    def timer_values(self) -> Tuple[int, int, int]:
        newDatetime = datetime.now() - self.start_time
        seconds = MAX_TIME - newDatetime.seconds
        minutes = seconds // 60
        secondsToPrint = seconds - minutes * 60
        return minutes, secondsToPrint, seconds

    @property
    def timer_text(self) -> str:
        minutes, secondsToPrint, seconds = self.timer_values()
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
        return "{}:{:2}".format(minutes, str(secondsToPrint).zfill(2))

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
        # send the new solenoid logic over I2C
        if value is SOLENOID_STATE.UNLOCKED:
            self.lock.open()
        else:
            self.lock.close()
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
    def keypad_code(self) -> hex:
        return self.shared.get("code", 0x000)

    @keypad_code.setter
    def keypad_code(self, value: hex):
        assert 0x0 <= value <= 0xfff
        log.debug("Setting new keypad code: 0x{}".format(value))
        self.shared["code"] = value

    @property
    def team(self) -> str:
        return self.shared.get("team", self.db.last.name if self.db.get_rows() else "--")

    @team.setter
    def team(self, value: str):
        log.debug("Setting current team name to: {}".format(value))
        self.shared["team"] = value
        if self.db.get_rows():
            self.db.last = Row(name=value)

    @property
    def rgb_color(self) -> RGBColor:
        return RGBColor(self.shared.get("rgb", RGBColor.BLANK.value))

    @rgb_color.setter
    def rgb_color(self, value: RGBColor):
        log.debug("Setting new rgb color: {}".format(value))
        # send the command over i2c to change the rgb color
        color_map = {'green': 0x1c, 'red': 0xe0, 'blue': 0x03, 'black': 0x00}
        self.arduino.color = color_map[value.value]
        self.shared["rgb"] = value.value

    def run(self, queue: Queue, mock: bool):
        """
        Start the game and make sure there is only a single instance of this process
        This is the setup function, when it is done, it will start the game loop
        """
        with self._process:
            # Initialize I2C server
            self.state = STATE.WAIT  # Change logic of game to WAIT
            self.solenoid = SOLENOID_STATE.LOCKED
            self.comQueue = queue
            self.ultrasonic = ULTRASONIC_STATE.ENABLED
            self.laserPattern = LaserPattern.ONE_CYCLES
            self.scheduler = APScheduler(scheduler=BackgroundScheduler(), app=current_app)
            self.scheduler.add_job("loop", self._loop, trigger='interval', seconds=1, max_instances=1,
                                   replace_existing=False)
            self.scheduler.start()

            # TODO start thread polling sensors
            try:
                while True:
                    self.poll_sensors()
            except KeyboardInterrupt:
                return

    def poll_sensors(self):
        """
        Poll all of the sensors and raise a flag if one of them has tripped.
        If the right wire was clipped at the end of the puzzle, raise the win flag
        """
        """
        for i in I2C:
            word = self._bus.read_byte_data(self.bus_num, i)
            if word is not None:
                # log.info("{}: {}".format(i.name, hex(word)))
                if i is I2C.RESET:
                    ComQueue().getComQueue().put([INTERRUPT.TOGGLE_TIMER])
                elif i is I2C.LASERS:
                    if self.laserValue != word:
                        ComQueue().getComQueue().put([INTERRUPT.KILL_PLAYER])
        """

        # self._bus.write_byte_data(I2C.LASERS.value, 0, 9) # for i2c in I2C:
        #     log.debug("Reading from I2C on {}".format(i2c.name))
        #     foo = self._bus.read_word_data(i2c.value, 0)
        #     self._send(I2C.SEVEN_SEG, "Hello!")

    def getNextLaserPatternList(self):
        if self.laserState is LaserPattern.ONE_CYCLES:
            return LaserPattern.TWO_CYCLES
        elif self.laserState is LaserPattern.TWO_CYCLES:
            return LaserPattern.UP_AND_DOWN
        elif self.laserState is LaserPattern.UP_AND_DOWN:
            return LaserPattern.INVERSION
        elif self.laserState is LaserPattern.INVERSION:
            return LaserPattern.LASER_OFF
        else:
            return self.laserState

    def getLaserPattern(self):
        if self.laserState is LaserPattern.ONE_CYCLES:
            pattern = LaserPatternValues.ONE_CYCLES.value
        elif self.laserState is LaserPattern.TWO_CYCLES:
            pattern = LaserPatternValues.TWO_CYCLES.value
        elif self.laserState is LaserPattern.UP_AND_DOWN:
            pattern = LaserPatternValues.UP_AND_DOWN.value
        elif self.laserState is LaserPattern.INVERSION:
            pattern = LaserPatternValues.INVERSION.value
        elif self.laserState is LaserPattern.LASER_OFF:
            pattern = LaserPatternValues.LASER_OFF.value
        elif self.laserState is LaserPattern.RANDOM:
            pattern = LaserPatternValues.RANDOM.value
        elif self.laserState is LaserPattern.STATIC:
            return self.laserValue
        else:
            pattern = None

        # Increment the patternIndex
        if pattern is not None:
            if self.patternIndex < len(pattern):
                retValue = pattern[self.patternIndex]
                self.patternIndex += 1
            else:
                self.patternIndex = 0
                retValue = pattern[self.patternIndex]

            if retValue == 0xFF:
                return random.randint(0, 0x3F)
            else:
                return retValue
        else:
            # All lasers turn
            return 0x3F

    def updateLaserPattern(self):
        if self.laserCounter < SECONDS_PER_PATTERN:
            self.laserCounterIncrement()
        else:
            self.laserState = self.getNextLaserPatternList()
            self.patternIndex = 0  # So that we start at the beginning
            self.laserCounter = 0

        # Time per element of pattern
        self.laserValue = self.getLaserPattern()

        # Set laser pattern
        self.lasers.state = self.laserValue

    def _loop(self):
        command_id = None
        if not self.comQueue.empty():
            command = self.comQueue.get()
            command_id = command[0]

        # State Actions
        if self.state is STATE.WAIT:
            self.sevenseg(0x0)
            self.laserState = LaserPattern.LASER_OFF
        elif self.state is STATE.RUNNING:
            minutes, seconds, total_seconds = self.timer_values()
            self.sevenseg(int("0x{:02}{:02}".format(minutes, seconds), 16))
            self.updateLaserPattern()
        elif self.state is STATE.EXPLODE:
            self.sevenseg(0xdead)
            # TODO randomize laser pattern so that they flash
        elif self.state is STATE.WIN:
            self.sevenseg(0xbeef)
        else:
            log.error("Reached an unknown state: {}".format(self.state))

        # State Transitions
        if self.state is STATE.WAIT:
            if command_id is INTERRUPT.TOGGLE_TIMER:
                # TODO? Verify that the box is reset before starting the game
                self.state = STATE.RUNNING
                self.start_game()
        elif self.state is STATE.RUNNING:
            if command_id is INTERRUPT.RESET_GAME or command_id is INTERRUPT.TOGGLE_TIMER:
                self.state = STATE.WAIT
                # FIXME? Delete last row on reset
                self.end_game(success=False)
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
        return random.randint(0, 0x40)

    def start_game(self):
        """
        Add a row to the database, generate random data for all the puzzles
        """
        self.solenoid = SOLENOID_STATE.LOCKED
        self.start_time = datetime.now()
        self.keypad_code = random.randint(0, 0xfff)
        self.rgb_color = random.choice([RGBColor.RED, RGBColor.BLUE])
        self.laserState = LaserPattern.ONE_CYCLES
        row = Row(
            name=self.team, lasers=self.laserValue, code=self.keypad_code, success=False, time=MAX_TIME,
            color=self.rgb_color.value,
        )
        log.debug("Adding new row to the database:\n{}".format(row))
        self.db.add_row(row)

    def end_game(self, success: bool = False):
        log.debug("Game Over")
        self.db.last = Row(
            name=self.team,
            code=self.keypad_code,
            lasers=self.laserValue,
            success=success,
            time=(datetime.now() - self.start_time).seconds
        )
