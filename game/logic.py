import logging
import random
from datetime import datetime
from multiprocessing import Lock, Manager, Queue
from typing import Tuple

from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
from flask_apscheduler import APScheduler
from os import path
from game.constants import I2C, STATE, RGBColor, INTERRUPT, SOLENOID_STATE, ULTRASONIC_STATE, MAX_TIME, LaserPattern, \
    SECONDS_PER_PATTERN, LaserPatternValues
from game.database import Database, Row
from globals import ComQueue
from Project_Theseus_API.i2c.laser_i2c import LaserControl
from Project_Theseus_API.i2c.lid_kit import ArduinoI2C
from Project_Theseus_API.i2c.receptors_i2c import ReceptorControl
from Project_Theseus_API.i2c.sevenseg import SevenSeg
from Project_Theseus_API.i2c.lock_i2c import BoxLock
from Project_Theseus_API.i2c.switches_i2c import SwitchesI2C
if path.exists("/dev/i2c-1"):
    from smbus2 import SMBus
else:
    from Project_Theseus_API.mockpi.smbus import MockBus as SMBus

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


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
    _command = None

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
        self.switches = SwitchesI2C(self._bus, I2C.SWITCHES)

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

    @property
    def command(self):
        return self.shared.get("command", None)

    @command.setter
    def command(self, value: str):
        self.shared["command"] = value

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
    def entered_code(self) -> hex:
        return self.shared.get("enteredcode", 0xFFF)

    @entered_code.setter
    def entered_code(self, value: hex):
        assert 0x0 <= value <= 0xfff
        log.debug("Setting new entered code: 0x{}".format(value))
        self.shared["enteredcode"] = value

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

    def run(self, queue: Queue):
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

    # Commented out because we are doing it in other functions
    def poll_sensors(self):
        """
        Poll all of the sensors and raise a flag if one of them has tripped.
        If the right wire was clipped at the end of the puzzle, raise the win flag
        """
        pass

        # self._bus.write_byte_data(I2C.LASERS.value, 0, 9) # for i2c in I2C:
        #     log.debug("Reading from Project_Theseus_API.i2c on {}".format(i2c.name))
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

    def checkCode(self):
        """
        Need to verify that the code they entered was correct.

        Verifies against the current keycode
        """
        # Get the last entered key
        key = self.arduino.keypad
        # The key should be a single hex character between 0 and 9
        # The entered_code variable stores the 3 numbers they have entered
        # If they enter a fourth number they die
        # Start Game initializes it to 0xFFF so we check that it isn't F
        # to see if a number has been previously entered
        str_keypad_code = "{:2X}".format(self.keypad_code)
        str_entered_code = "{:2X}".format(self.entered_code)

        # Iterate through characters and verify
        for i in range(0, 3):
            # Add latest key to entered code
            if str_entered_code[i] == "F":
                if key != None:
                    # We need to fill this space
                    str_entered_code[i] = key
                    # Save in the shared dict
                    self.entered_code = int(str_entered_code)

                    # Now we need to check if it matches
                    if str_entered_code[i] != str_keypad_code[i]:
                        return False
                    else:
                        # The key matched so far, continue
                        pass
                else:
                    # Key was none, don't update entered and don't check
                    pass

            else:
                # entered code is not F, so we need to see if it matches
                # admitedly this shouldn't be called because of how we check
                if str_entered_code[i] != str_keypad_code[i]:
                    return False

        # We are assuming it has matched so far, but if they have entered another key,
        # it no longer does, and they should fail
        if key != None:
            return False
        else:
            # They didn't type a key, so they lived and won
            # They didn't exceed the code size
            # TODO: Add additional code for more logic later, this will
            # make them win right now
            self.state = STATE.WIN
            self.end_game(success=True)
        # If you reached here, the codes matched so far, so return True
        return True

    def updateLed(self):
        """
        There are 6 switches on the box. The four black correspond to a number
        in hex, and the 2 white help you know which number in the keypad_code
        you are looking at. The light will be RED if the white switches are 0
        or the current code is wrong, and GREEN if the corresponding number from
        keypad_code is correct.
        """
        # TODO: Verify that my understanding of how the switches are organized
        # as far as the number they return is correct

        # Determined by the white switches. 0 corresponds to none of the numbers
        # and 1, 2, and 3 respectively correspond to the 1, 2, and 3 numbers in
        # keypad_code
        keypad_code_index = self.switches.read_switches()[-2:]
        # What number does the user want to test?
        test_number = self.switches.read_switches()[:-2]
        # Get the keypad code as a string
        str_keypad_code = "{:2X}".format(self.keypad_code)

        # set the led based on if they are correct
        if keypad_code_index > 0:
            if str_keypad_code[keypad_code_index - 1] == str(test_number):
                # It matches, make the light green
                self.rgb_color = RGBColor.GREEN
            else:
                # It doesn't match, make the light red
                self.rgb_color = RGBColor.RED
        else:
            # They haven't selected one, make it blue
            self.rgb_color = RGBColor.BLUE


    def _loop(self):
        command_id = None
        if not self.comQueue.empty():
            command = self.comQueue.get()
            command_id = command[0]
            print("\n\n\n{}\n\n\n".format(command_id))

        # State Actions
        if self.state is STATE.WAIT:
            self.sevenseg(0x0)
            self.laserState = LaserPattern.LASER_OFF
        elif self.state is STATE.RUNNING:
            # Update the seven segment display to show the correct time
            minutes, seconds, total_seconds = self.timer_values(self.sevenseg(int("0x{:02}{:02}".format(minutes, seconds), 16)))
            # Update what the current laser pattern should be
            self.updateLaserPattern()
            # Update LED by checking switches
            self.updateLed()

        elif self.state is STATE.EXPLODE:
            self.sevenseg(0xdead)
            # TODO randomize laser pattern so that they flash
        elif self.state is STATE.WIN:
            self.sevenseg(0xbeef)
        else:
            log.error("Reached an unknown state: {}".format(self.state))

        # State Transitions
        if self.state is STATE.WAIT:
            if self.command == "toggle-game":
                self.command = None
                # TODO? Verify that the box is reset before starting the game
                self.state = STATE.RUNNING
                self.start_game()
        elif self.state is STATE.RUNNING:
            minutes, seconds, total_seconds = self.timer_values()

            if self.command == "toggle-game" or self.command == "toggle-game":
                if self.command is not None:
                    self.command = None
                self.state = STATE.WAIT
                # FIXME? Delete last row on reset
                self.end_game(success=False)
            elif command_id is INTERRUPT.KILL_PLAYER:
                self.state = STATE.EXPLODE
                self.end_game(success=False)
            elif command_id is INTERRUPT.DEFUSED:
                self.state = STATE.WIN
                self.end_game(success=True)

            # Kill the player if time has run out
            elif total_seconds <= 0:
                self.state = STATE.EXPLODE
                self.end_game(success=False)

            elif self.laserValue != self.photo_resistors.read_int():
                self.state = STATE.EXPLODE
                self.end_game(success=False)

            elif not self.checkCode():
                # If they reached here the code didn't match
                self.state = STATE.EXPLODE
                self.end_game(success=False)

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
        return random.randint(0, 0x40)

    def generateKeyCode() -> int:
        """
        Generate a 3 number code where all numbers are less than 9 and >= 0
        """
        # We can't go over 9 because our keypad doesn't go above 9
        return (random.randint(0, 0x9) << 8) | (random.randint(0, 0x9) << 4) | (random.randint(0, 0x9))


    def start_game(self):
        """
        Add a row to the database, generate random data for all the puzzles
        """
        self.solenoid = SOLENOID_STATE.LOCKED
        self.start_time = datetime.now()
        self.keypad_code = generateKeyCode()
        self.entered_code = 0xFFF       # Set as this because it is impossible to get on our keypad
        self.rgb_color = RGBColor.BLUE
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
