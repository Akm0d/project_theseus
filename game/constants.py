import datetime
from enum import Enum, IntEnum


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
class COMMUNICATION(Enum):
    DEFUSED = "Yay I won!!!!"                       # The device was successfully defused
    TOGGLE_TIMER = "toggle-timer"                   # Toggle if timer is on/off
    TIMER_TOGGLED = "timer-toggled"                 # Confirmation of timer toggle
    START_GAME = "start-game"
    RESET_GAME = "reset-game"
    KILL_PLAYER = "kill-player"                     # Player has died


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
    # TOP Lid
    KEYPAD = 0x0b
    SEVEN_SEG = 0x0c


class SOLENOID_STATE(IntEnum):
    LOCKED = 1
    UNLOCKED = 0


class ULTRASONIC_STATE(IntEnum):
    ENABLED = 1
    DISABLED = 0


# The Time the timer should be reset to in seconds.  Defaults to 3 minutes
TIME_GIVEN = 180
# What is no time left?
TIME_OVER = datetime.datetime.strptime("00:00", "%M:%S")


# What are valid values for the RGB LEDS
class RGBColor(Enum):
    GREEN = "green"
    RED = "red"
    BLUE = "blue"
    BLANK = "black"


class JSCom(Enum):
    START_BUTTON = "Start"
    RESET_BUTTON = "Reset"
