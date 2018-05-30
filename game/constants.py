from enum import Enum, IntEnum

# The Time the timer should be reset to in seconds.  Defaults to 3 minutes
MAX_TIME = 180


# What are the logical states for the logic machine
class STATE(Enum):
    # INIT event goes to WAIT
    WAIT = "wait"
    # WAIT goes to RUNNING on PLAY
    RUNNING = "run"
    # RUNNING goes to either WIN or EXPLODE depending on if
    # It recieves a SUCCESS or a FAILURE
    WIN = "win"
    EXPLODE = "explode"
    # EXPLODE and WIN go to WAIT on RESET


# How often should the logic _loop function run
INTERRUPTS_PER_SECOND = 10
# How long should the sleep interval be inbetween runs of _loop
SLEEP_INTERVAL = 1 / INTERRUPTS_PER_SECOND


# Communication between processes must be one of these
class INTERRUPT(Enum):
    DEFUSED = "Yay I won!!!!"  # The device was successfully defused
    TOGGLE_TIMER = "toggle-timer"  # Toggle if timer is on/off
    RESET_GAME = "reset-game"
    KILL_PLAYER = "kill-player"  # Player has died


# What are the events that trigger transitions between each logic
class EVENTS(Enum):
    INIT = "init"
    PLAY = "play"
    SUCCESS = "success"
    FAILURE = "failure"
    RESET = "reset"


class I2C(IntEnum):
    """
    I2C addresses of each slave device
    """
    # Sensors
    FLEX = 0x03
    IMU = 0x04
    ULTRASONIC = 0x05
    # Laser tripwires
    LASERS = 0x06
    PHOTO_RESISTORS = 0x07
    # Inner box lid puzzle
    ROTARY = 0x08
    SWITCHES = 0x09
    LEDS = 0x0a
    WIRE = 0x0b
    # TOP Lid
    KEYPAD = 0x0c
    SEVEN_SEG = 0x0d
    # Outer box
    RESET = 0x0e


class SOLENOID_STATE(IntEnum):
    LOCKED = 1
    UNLOCKED = 0


class ULTRASONIC_STATE(IntEnum):
    ENABLED = 1
    DISABLED = 0


# What are valid values for the RGB LEDS
class RGBColor(Enum):
    GREEN = "green"
    RED = "red"
    BLUE = "blue"
    BLANK = "black"


class JSCom(Enum):
    START_BUTTON = "Start"
    RESET_BUTTON = "Reset"


class LaserPattern(Enum):
    ONE_CYCLES = "one_cycles"   # One laser cycles diwb
    TWO_CYCLES = "two_cycles"   # Two (separated by one) move down slowly.
    UP_AND_DOWN = "up_and_down" # Top and bottom turn on, move to the center than back out
    INVERSION = "inversion"     # Every other is turned on and then every second, they invert
    LASER_OFF = "laser_off"     # No laser is active
    STATIC = "static"           # Lasers stay at what admin sets them
    RANDOM = "random"           # Lasers turn on and off randomly

class LaserPatternValues(Enum):
    ONE_CYCLES = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20]
    TWO_CYCLES = [0x05, 0x0A, 0x14, 0x28, 0x11, 0x22]
    UP_AND_DOWN = [0x21, 0x12, 0x0C, 0x12]
    INVERSION = [0x2A, 0x15]
    LASER_OFF = [0x00]
    RANDOM = [0xFF]

SECONDS_PER_PATTERN = 45        # Time each laser pattern runs
SECONDS_PER_CHANGE = 1          # How often does the pattern change

# What is the order for the patterns to change by
PATTERN_LIST = [LaserPatternValues.ONE_CYCLES, LaserPatternValues.TWO_CYCLES, LaserPatternValues.UP_AND_DOWN, LaserPatternValues.INVERSION]
