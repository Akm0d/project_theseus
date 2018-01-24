SUCCESS = 's'
FAILURE = 'f'
HEARTBEAT = 'h'
ALIVE = 'a'
RECEIVE = 'c'

# Buttons
RESET_TIMER, RESET_ALL, RESET_CONNECTIONS, START_TIMER, BREAK, TOGGLE_DEBUG, START_RESET = "1", "2", "3", "4", "5", "6", "7"
AVAILABLE_COMMANDS = {
#    'Timer Reset': RESET_TIMER,
#    'Reset All': RESET_ALL,
    'Toggle Debug': TOGGLE_DEBUG,
    'Reconnect': RESET_CONNECTIONS,
#    'Timer Start': START_TIMER,
    'START/RESET': START_RESET,
    'Break': BREAK,
    'TOGGLE ULTRASONIC':'TOGGLE ULTRASONIC'
}

# Arduino Send/Receive constants
KNOCK_KIT = 1
KNOCK_KIT_ULTRASONIC_TRIP = 'u'

PUZZLE_KIT = 2
PUZZLE_KIT_CORRECT = "c"
PUZZLE_KIT_CORRECT_OFF = "o"
PUZZLE_KIT_RANDOMIZE = "r"
PUZZLE_KIT_LOCK = "l"
PUZZLE_KIT_UNLOCK = "u"
PUZZLE_KIT_POT_VALUE = 'p'
PUZZLE_KIT_SWITCH_VALUE = 'w'
PUZZLE_KIT_DEAD_ZONE = 'Z'
PUZZLE_KIT_RED_WIRE = 'R'
PUZZLE_KIT_BLUE_WIRE = 'B'


LID_KIT = 3
LID_KIT_TIMER_RESET = "r"
LID_KIT_TIMER_START = "t"
LID_KIT_TIMER_DEAD = "d"
LID_KIT_RGB_BLUE = "B"
LID_KIT_RGB_RED = "R"
LID_KIT_RGB_GREEN = "G"
LID_KIT_RGB_OFF = "O"
LID_KIT_KEYPRESS = 'k'
LID_KIT_TICK = 'T'

LED_KIT = 4
LED_KIT_TRIPPED = "T"
LED_KIT_STRIP_ON = "N"
LED_KIT_STRIP_OFF = "F"
LED_KIT_RANDOMIZE = "R"


# DEBUG LEVELS
NONE, ERROR, WARN, INFO, EVENTS = 0, 1, 2, 4 ,8
DEBUG_COMMANDS = {
    'WARN':'WARN',
    'ERROR':'ERROR',
    'INFO':'INFO',
    'EVENTS':'EVENTS'
}


# Drop down menus
KNOCK_KIT_COMMANDS = {
}

RGB_BLUE = "RGB: Blue"
RGB_RED = "RGB: Red"
RGB_GREEN = "RGB: Green"
RGB_OFF = "RGB: Off"
DEAD = "Dead"
LID_KIT_COMMANDS = {
    'rgb_red': RGB_RED, 'rgb_blue': RGB_BLUE,
    'rgb_green': RGB_GREEN,
    'rgb_off': RGB_OFF,
    'dead': DEAD
}

RANDOMIZE_LASERS = "Randomize Lasers"
LEDSTRIP_ON = "LED Strip ON"
LEDSTRIP_OFF = "LED Strip Off"
LED_KIT_COMMANDS = {
    'randomize_lasers': RANDOMIZE_LASERS,
    'ledstrip_on': LEDSTRIP_ON,
    'ledstrip_off': LEDSTRIP_OFF
}

UNLOCK_SOLENOID = "Unlock Solenoid"
LOCK_SOLENOID = "Lock Solenoid"
CORRECT = "Correct"
PUZZLE_KIT_COMMANDS = {
    'unlock_solenoid': UNLOCK_SOLENOID,
    'lock_solenoid': LOCK_SOLENOID,
    'correct': CORRECT
}

INITIAL_TIME = 10
UPDATE_TIMER_MAX = 100
UPDATE_ARDUINO_MAX = .01

SEND_TICK_MAX = 100

MAX_HISTORY_SIZE = 10

DEAD_SPACE_VALUE = '3'

DEAD_SWITCH_TEST = 16

SWITCH_VALUE = {'`': 31,
                '_': 30,
                '^': 29,
                ']': 28,
                '\\': 27,
                '[': 26,
                'Z': 25,
                'Y': 24,
                'X': 23,
                'W': 22,
                'V': 21,
                'U': 20,
                'T': 19,
                'S': 18,
                'R': 17,
                'Q': 16,
                'P': 15,
                'O': 14,
                'N': 13,
                'M': 12,
                'L': 11,
                'K': 10,
                'J': 9,
                'I': 8,
                'H': 7,
                'G': 6,
                'F': 5,
                'E': 4,
                'D': 3,
                'C': 2,
                'B': 1,
                'A': 0
                }
