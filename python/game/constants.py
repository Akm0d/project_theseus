from enum import Enum, IntEnum
import datetime

# What are the logical states for the state machine
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

INTERRUPTS_PER_SECOND = 10
SLEEP_INTERVAL = 1 / INTERRUPTS_PER_SECOND

# What are the events that trigger transitions between each state
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


TIME_GIVEN = datetime.datetime.strptime("03:00", "%M:%S")
TIME_OVER = datetime.datetime.strptime("00:00", "%M:%S")
