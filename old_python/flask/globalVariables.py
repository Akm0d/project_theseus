from queue import Queue

from functions.timer import Timer
from functions.wires import Wires
from functions.keypad import Keypad
from static.constants import *
import pickle,os.path

if os.path.isfile("top_scores.pkl"):
    top_scores = pickle.load( open( "top_scores.pkl", "rb" ) )
else:
    #top_scores = {'scores': [("Tyler", 100), ("Bob", 89)], 'attempts': 30}
    top_scores = {'scores': [], 'attempts': 0}

def increment_attempts():
    top_scores['attempts'] = top_scores.get('attempts', 0) + 1
    pickle.dump( top_scores, open( "top_scores.pkl", "wb" ) )

use_watchdog = False

def getWatchdog():
    global use_watchdog
    return use_watchdog

def setWatchdog(value):
    global use_watchdog
    return use_watchdog

# This is the data that gets passed to the webserver.  It is printed
# in the console
output = []

debug = WARN | INFO | ERROR | EVENTS

def getDebug():
    global debug
    return debug

def setDebug(value):
    global output
    debug = int(value)

prevSwitchValue = None

def getPrevSwitchValue():
    global prevSwitchValue
    return prevSwitchValue

def setPrevSwitchValue(newValue):
    global prevSwitchValue
    prevSwitchValue = newValue

def switchHasChanged(newValue):
    global prevSwitchValue
    return prevSwitchValue != newValue

prevPotValue = None

def setPrevPotValue(newValue):
    global prevPotValue
    prevPotValue = newValue

def potHasChanged(newValue):
    global prevPotValue
    return prevPotValue != newValue

# This is the variable that holds the keycode that must be typed in
keypad = Keypad()

def keypadGenerateKeys(switchValue):
    global keypad
    keypad.generateKeys(switchValue)

def keypadGetKey(index):
    global keypad
    return keypad.getKey(index)

def keypadSetCombo(newCombo):
    global keypad
    keypad.setCombo(newCombo)

def keypadCheckKey(keystroke, index):
    global keypad
    return keypad.checkKey(keystroke, index)

def keypadCheckCombo(entryList):
    global keypad
    return keypad.checkCombo(entryList)

def keypadSprintCombo():
    global keypad
    return keypad.sprintCombo()

def keypadPrintCombo():
    global keypad
    keypad.printCombo()

# This is what holds the timer info for the webserver
timerObject = Timer(INITIAL_TIME)

def getTimer():
    global timerObject
    return timerObject

def resetTimer():
    global timerObject
    timerObject.reset()

def OOT_flag():
    global timerObject
    timerObject.outOfTime()

def decSecTimer():
    global timerObject
    timerObject.decrementSecond()

def decTenthSecTimer():
    global timerObject
    timerObject.decrementTenthSecond()

def sprintTimer():
    global timerObject
    return timerObject.sprintTimer()

def printTimer():
    global timerObject
    print(timerObject.sprintTimer())

# Variable used to determine if the machine is running (test has begun)
timer_running = False

def get_timer_running():
    global timer_running
    return timer_running

def set_timer_running(value):
    global timer_running
    timer_running = value

# A variable that holds which wire must be cut at the end.  BLue or Red
wire = Wires()

def getWire():
    global wire
    return wire

def randomizeWire():
    global wire
    wire.randomize_wire()

# Value must be BLUE_WIRE or RED_WIRE
def checkWire(value):
    global wire
    return wire.check_wire(value)

def getWireColor():
    global wire
    return wire.getColor()

### Arduino Variables ###
# A queue of button presses received from the touchpad
touchpad_input = list()

def append_touchpad_input(value):
    global touchpad_input
    touchpad_input.append(value)

def getObject_touchpad_input():
    global touchpad_input
    return touchpad_input

def getSize_touchpad_input():
    global touchpad_input
    return len(touchpad_input)

def getIndex_touchpad_input(index):
    global touchpad_input
    return touchpad_input(index)

def clear_touchpad_input():
    global touchpad_input
    touchpad_input.clear()

def getLen_touchpad_input():
    global touchpad_input
    return len(touchpad_input)


ultrasonic_en = True
def toggle_ultrasonic():
    global ultrasonic_en
    if ultrasonic_en:
        ultrasonic_en = False
    else: 
        ultrasonic_en = True

def get_ultrasonic():
    global ultrasonic_en
    return ultrasonic_en

# Variable that stores what the current value of the pot value is
pot_value = 0

def get_pot_value():
    global pot_value
    return pot_value

def set_pot_value(newValue):
    global pot_value
    pot_value = newValue

# Value of the wire that is cut.  Starts as None because wires don't start cut
wire_value = None

def set_wire_value(cutWire):
    global wire_value
    wire_value = cutWire

def resetWireValue():
    global wire_value
    wire_value = None

def get_wire_value():
    global wire_value
    return wire_value

# a single byte that represents the last seen value of the switches
switches_char = None

def set_switches_char(new_char):
    global switches_char
    switches_char = new_char

def get_switches_char():
    global switches_char
    return switches_char

# An int that represents the last seen position of the potentiometer
pot_position = None

def set_pot_position(pot):
    global pot_position
    pot_position = pot

def get_pot_position():
    global pot_position
    return pot_position

# Variable used to determine if some event has caused the death of the
# Player
dead = False

def set_dead(b_value):
    global dead
    dead = b_value


def get_dead():
    global dead
    return dead
