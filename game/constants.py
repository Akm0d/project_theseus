from enum import Enum, IntEnum
import datetime
import logging

# The Time the timer should be reset to in seconds.  Defaults to 3 minutes
MAX_TIME = 180


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

# How often should the logic _loop function run
INTERRUPTS_PER_SECOND = 10
# How long should the sleep interval be inbetween runs of _loop
SLEEP_INTERVAL = 1 / INTERRUPTS_PER_SECOND

# Communication between processes must be one of these
class COMMUNICATION(Enum):
    TOGGLE_TIMER = "toggle-timer"                   # Toggle if timer is on/off
    TIMER_TOGGLED = "timer-toggled"                 # Confirmation of timer toggle
    GET_STATE = "get-state"                         # Please send me the state
    SENT_STATE = "sent-state"                       # Message includes state
    GET_TIMER = "get-timer-text"                    # Please get the timer text
    TIMER_TEXT = "timer-text"                       # Message contains timer text
    START_GAME = "start-game"
    TOGGLE_SOLENOID = "toggle-solenoid"             # Toggle if solenoid is open or closed
    SOLENOID_STATUS = "solenoid-status"             # Please send state of solenoid
    SENT_SOLENOID_STATUS = "sent-solenoid-status"   # Message contains state of solenoid
    GET_ACTIVATED_LASERS = "get-activated-lasers"   # Please send the laser state (which are lit up)
    ACTIVATED_LASERS = "activated-lasers"           # Message will include current laser state
    TOGGLE_LASER = "toggle-laser"                   # trigger toggle of specified laser
    RANDOMIZE_LASERS = "randomize-lasers"           # Randomize lasers and return state
    ALL_LASERS = "all-lasers"                       # Do something to all lasers
    GET_CODE = "get-code"                           # Get current hex code
    SENT_CODE = "sent-code"                         # Message contains current code in Logic
    SET_CODE = "set-code"                           # Change hex code to what is included
    GET_RGB = "get-rgb"                             # What is the current color of the RGB?
    SENT_RGB = "sent-rgb"                           # Message contains RGB color
    SET_RGB = "set-rgb"                             # Set RGB to specified color
    GET_TEAM = "get-team"                           # What team is currently working?
    SENT_TEAM = "sent-team"                         # Message includes current team
    SET_TEAM = "set-team"                           # Set what team will work
    TOGGLE_ULTRASONIC = "toggle-ultrasonic"         # Toggle whether the ultrasonic is active or not
    GET_ULTRASONIC = "get-ultrasonic"               # Return current ultrasonic state
    SENT_ULTRASONIC = "sent-ultrasonic"             # Message includes state of ultrasonic

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


class SOLENOID_STATE(Enum):
    LOCKED = "locked"
    UNLOCKED = "unlocked"


# How much time do they start with?
TIME_GIVEN = datetime.datetime.strptime("03:00", "%M:%S")
# What is no time left?
TIME_OVER = datetime.datetime.strptime("00:00", "%M:%S")

# What are valid values for the RGB LEDS
class RGBColor(Enum):
    GREEN = "green"
    RED = "red"
    BLUE = "blue"
    BLANK = "blank"


LOGGING_LEVEL = logging.ERROR
