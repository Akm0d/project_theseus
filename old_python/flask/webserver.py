#!/usr/bin/env python3
# coding=utf-8
from static.constants import *
from static.messages import *
import threading
import time
import functions.SerialTerminal as serial
from globalVariables import *
import argparse
import flask
import os

parser = argparse.ArgumentParser()
parser.add_argument('--host', help='The host name or ip address to run on', type=str, default='0.0.0.0')
parser.add_argument('--port', help='The port number the web server will use', type=int, default=5000)
parser.add_argument('--cert', help='The SSL certificate', type=str)
parser.add_argument('--key', help='The SSL private key', type=str)
parser.add_argument('-d', '--debug', help='Enable debugging mode', action="store_true")
parser.add_argument('-v', '--verbose', help='Enable verbose mode', action="store_true")
args = parser.parse_args()

SECURE = bool(args.cert) and bool(args.key)

output = ["Initialized console"]
output.extend(serial.get_output())
history = []

app = flask.Flask(__name__)
arduino = None

def history_add(item):
    """
    Keep history trim
    :param item: string to add to history
    """
    while len(history) >= MAX_HISTORY_SIZE:
        history.pop(0)
    history.append(item)


@app.route('/favicon.ico')
def favicon():
    """
    :return: The favicon image found in static/favicon.ico
    """
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),
                                     'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/")
def index():
    """
    Redirects to the timer page, which is the default
    :return:
    """
    text = "stuff"
    return flask.redirect("/timer")


@app.route("/update-timer-value/")
def updateTimerValue():
    """
    Used to update the timer using JS so that the entire page
    doesn't have to reload.
    """
    return flask.render_template('timer.html',
                                 timer=sprintTimer())


@app.route("/attempts/")
def updateAttempts():
    """
    Used to update the attempts using JS so that the entire page
    doesn't have to reload.
    """
    return flask.render_template('attempts.html',
                                 attempts=top_scores.get('attempts'))

@app.route("/timerPage")
def timer():
    """
    This is the default webpage that contestant's will see
    :return: the timer's html page

    It is designed to change the color of the timer based on how
    much time they have left.
    GREEN   > 1 minute
    YELLOW  > 30 seconds, < 1 minute
    RED     < 30 seconds
    """

    color = "green"
    return flask.render_template('timerPage.html',
                                 title="Defusal Station: Timer",
                                 timer=sprintTimer(),
                                 textColor=color,
                                 attempts=top_scores.get('attempts'),
                                 scores=top_scores.get('scores'),
                                 refreshEvery=5000)

def read_output():
    global output
    # TODO this needs to be handled with a semaphore
    output.extend(serial.get_output())
    while output:
        item = output.pop(0)
        history_add(item)
        yield "data:" + item + "\n\n"

updateTick = 0

# TODO Once I have this working so good, we can have a button or slider that filters output based on debug level
# TODO This should definitely ignore heartbeats, or just don't send heartbeats to this
# TODO Add sampling of global variables
def output_reading_thread():
    global updateTick
    global arduino
    while True:
        if get_dead():
            arduino.send_data(LID_KIT, LID_KIT_TIMER_DEAD)
            arduino.send_data(LED_KIT, LED_KIT_STRIP_ON)

            # Turn off the Wire indicating LED
            arduino.send_data(LID_KIT, LID_KIT_RGB_OFF)

            set_timer_running(False)
            set_dead(False)
            clear_touchpad_input()

            # Turn off the switch value correct LED
            arduino.send_data(PUZZLE_KIT, PUZZLE_KIT_CORRECT_OFF)
        
        if arduino is None:
            # App variables
            arduino = serial.ArduinoSerial()
            arduino.list_devices()

        arduino.receive_data()
        if get_timer_running():
            # This function must change based on what the delay is.
            # Right now it is A tenth of a second
            if updateTick < SEND_TICK_MAX:
                updateTick = updateTick + 1
            else:
                updateTick = 0
                decSecTimer()
                arduino.send_data(LID_KIT, LID_KIT_TICK)

            # First, get the current value on the switches
            curSwitchValue = get_switches_char()
            curPotValue = get_pot_value()

            if curSwitchValue is not None and curPotValue is not None:
                if (switchHasChanged(curSwitchValue) or potHasChanged(curPotValue)):
                    if SWITCH_VALUE.get(curSwitchValue) >= DEAD_SWITCH_TEST:
                        set_dead(True)
                    else:
                        if (keypadCheckKey(ord(curSwitchValue) - ord('A'), curPotValue)):
                            arduino.send_data(PUZZLE_KIT, PUZZLE_KIT_CORRECT)
                        else:
                            arduino.send_data(PUZZLE_KIT, PUZZLE_KIT_CORRECT_OFF)
                else:
                    # Nothing has changed
                    pass
            else:
                # Either pot or the switch has not been set
                pass

            # Check if the wire is cut, if it is, declare them a winner
            if get_wire_value() is not None:
                if checkWire(get_wire_value()):
                    # WIN STATE, THE PLAYER HAS WON
                    arduino.send_data(LID_KIT, LID_KIT_RGB_GREEN)
                    set_timer_running(False)
                else:
                    # They clipped the wrong wire
                    set_dead(True)

        # TODO This is the function that records the score
        time.sleep(UPDATE_ARDUINO_MAX)


# https://mortoray.com/2014/03/04/http-streaming-of-command-output-in-python-flask
@app.route('/console')
def console():
    """
    Constantly stream data to the admin console
    This update happens once a second when really it should happen any time there is a new message
    :return:
    """
    return flask.Response(read_output(), mimetype='text/event-stream')

def reset_timer():
    if getDebug() & INFO: output.append(RESET_TIMER_M)
    # Reset timerObject to 10 minutes
    set_timer_running(False)
    resetTimer()
    arduino.send_data(LID_KIT, LID_KIT_TIMER_RESET)
    arduino.send_data(PUZZLE_KIT, PUZZLE_KIT_LOCK)
    set_wire_value(None)

    # Erase all memory of input from keypad
    clear_touchpad_input()

    # Set dead to False
    set_dead(False)
    clear_touchpad_input()

    # Send dead signal to LED_STRIP
    arduino.send_data(LED_KIT, LED_KIT_STRIP_OFF)

    # Turn off wire LED
    arduino.send_data(LID_KIT, LID_KIT_RGB_OFF)
    
    # Reset switches_char
    set_switches_char(None)

    # Reset pot
    set_pot_position(None)

def start_timer():
    # Start the timer running
    increment_attempts()
    history.append(START_TIMER_M)
    if getDebug() & INFO: output.append(START_TIMER_M)

    set_timer_running(True)
    arduino.send_data(LID_KIT, LID_KIT_TIMER_START)

    # Set the lasers
    history.append(RANDOM_LASERS_M)
    arduino.send_data(LED_KIT, LED_KIT_RANDOMIZE)

    arduino.send_data(LED_KIT, LED_KIT_STRIP_OFF)

    # Randomize and save new key
    keypadGenerateKeys(switches_char)
    print(keypadSprintCombo())

    set_dead(False)
    clear_touchpad_input()

    # Pick either white or orange wire
    history.append(RANDOM_WIRE_M)
    if getDebug() & INFO: output.append(RANDOM_WIRE_M)
    randomizeWire()

    if (getWireColor() == PUZZLE_KIT_BLUE_WIRE):
        # Send to the RGB LED in the lid, what color was chosen
        arduino.send_data(LID_KIT, LID_KIT_RGB_BLUE)
    else:
        arduino.send_data(LID_KIT, LID_KIT_RGB_RED)


# This is where buttons will actually change things
# Possibly add buttons for sending signals to the different arduinos
# This way, the python will send only exactly what the arduinos expect
# Have a carousel for selecting an arduino
# For the selected item in the carousel, have a second carousel that has available commands for that arduino
@app.route('/<cmd>')
def command(cmd=None):
    """
    Handles button presses from the admin page.
    These buttons are defined in AVAILABLE_COMMANDS
    :param cmd: The id of the button that was pressed on the admin page
    :return: Nothing really, just stay on the same page
    """
    global output
    if cmd == RESET_TIMER:
        reset_timer()
    elif cmd == RESET_ALL:
        # TODO Power cycle the raspberry pi
        # Or reset the script by setting the startup command to start after a delay
        # And then pkill all python
        if getDebug() & INFO: output.append("This button does nothing yet")
        #if getDebug(): output.append(REBOOT_DEVICE_M)
        #if getDebug(): output.append(LINE_DOTS_M)
    elif cmd == RESET_CONNECTIONS:
        set_timer_running(False)
        arduino.reset()
    elif cmd == START_RESET:
        if get_timer_running():
            reset_timer()
        else:
            start_timer()

        pass
    elif cmd == START_TIMER:
        start_timer()
    elif cmd == 'TOGGLE ULTRASONIC':
        if get_ultrasonic():
            output.append("Disabling ultrasonic")
        else:
            output.append("Enbling ultrasonic")
        toggle_ultrasonic()
    elif cmd == BREAK:
        Break()

    if getDebug(): output.extend(serial.get_output())
    return "", 200, {'Content-Type': 'text/plain'}


@app.route('/send_command', methods=['GET', 'POST'])
def send_command():
    form_data = flask.request.form.to_dict()
    kit = form_data['arduino']
    #if kit == "knock_kit":
        #history.append(KNOCK_KIT_COMMANDS_M)
    if kit == "puzzle_kit":
        cmd = flask.request.form["puzzle_kit_command"]
        if cmd == LOCK_SOLENOID:
            history.append(LOCK_SOLENOID_M)
            arduino.send_data(PUZZLE_KIT, PUZZLE_KIT_LOCK)
        elif cmd == UNLOCK_SOLENOID:
            history.append(UNLOCK_SOLENOID_M)
            arduino.send_data(PUZZLE_KIT, PUZZLE_KIT_UNLOCK)
        elif cmd == PUZZLE_KIT_RANDOMIZE:
            if getDebug() & EVENTS: output.append(RANDOMIZE_PUZZLE_M)
            # TODO Generate random puzzle data
            # Maybe do it on the arduino, and have the arduino report it back
            arduino.send_data(PUZZLE_KIT, PUZZLE_KIT_RANDOMIZE)
        elif cmd == CORRECT:
            if getDebug() & EVENTS: output.append(CORRECT_VALUE_M)
            arduino.send_data(PUZZLE_KIT, PUZZLE_KIT_CORRECT)
        elif cmd == INCORRECT:
            if getDebug() & EVENTS: output.append(INCORRECT_VALUE_M)
            arduino.send_data(PUZZLE_KIT, PUZZLE_KIT_CORRECT_OFF)
    elif kit == "lid_kit":
        cmd = flask.request.form["lid_kit_command"]
        if cmd == DEAD:
            history.append(SIGNAL_DEAD_M)
            arduino.send_data(LID_KIT, LID_KIT_TIMER_DEAD)
        elif cmd == RGB_BLUE:
            history.append(RGB_BLUE_M)
            arduino.send_data(LID_KIT, LID_KIT_RGB_BLUE)
        elif cmd == RGB_GREEN:
            history.append(RGB_GREEN_M)
            arduino.send_data(LID_KIT, LID_KIT_RGB_GREEN)
        elif cmd == RGB_RED:
            history.append(RGB_RED_M)
            arduino.send_data(LID_KIT, LID_KIT_RGB_RED)
        elif cmd == RGB_OFF:
            history.append(RGB_OFF_M)
            arduino.send_data(LID_KIT, LID_KIT_RGB_OFF)
    elif kit == "led_kit":
        cmd = flask.request.form["led_kit_command"]
        if cmd == RANDOMIZE_LASERS:
            history.append(RANDOM_LASERS_M)
            arduino.send_data(LED_KIT, LED_KIT_RANDOMIZE)
        elif cmd == LEDSTRIP_ON:
            history.append(LED_STRIP_ON_M)
            arduino.send_data(LED_KIT, LED_KIT_STRIP_ON)
        elif cmd == LEDSTRIP_OFF:
            history.append(LED_STRIP_OFF_M)
            arduino.send_data(LED_KIT, LED_KIT_STRIP_OFF)
    elif kit == "debug_command":
        if cmd == "WARN":
            setDebug(getDebug() ^ WARN)
            history.append("TOGGLING DEBUG WARN")
        elif cmd == "ERROR":
            setDebug(getDebug() ^ ERROR)
            history.append("TOGGLING DEBUG ERROR")
        elif cmd == "INFO":
            setDebug(getDebug() ^ INFO)
            history.append("TOGGLING DEBUG INFO")
        elif cmd == "EVENTS":
            setDebug(getDebug() ^ EVENTS)
            history.append("TOGGLING DEBUG EVENTS")
        pass
    if getDebug() & INFO:
        output.extend(history)
    history.clear()
    return flask.redirect('/admin')


def Break(length=60):
    """
    :param length: The number of characters in the break line
    """
    output.append("=" * int(length))
    pass


@app.route("/admin")
def admin():
    """
    :return: A rendering of the admin page
    AVAILABLE_COMMANDS: list that contains all the buttons that should be created
    """
    return flask.render_template('admin.html', title="Defusal Station: Admin", commands=AVAILABLE_COMMANDS,
                                 debug_commands=DEBUG_COMMANDS, lid_kit_commands=LID_KIT_COMMANDS,
                                 puzzle_kit_commands=PUZZLE_KIT_COMMANDS, led_kit_commands=LED_KIT_COMMANDS)


if __name__ == "__main__":
    """
    Start the web server, use https if certificates were supplied
    TODO start the thread that automates control of the defusal station
    """
    # Display basic info based on command line arguments
    if args.verbose: print("Verbose mode activated")
    if args.debug: print("Debug mode activated")
    if bool(args.cert) != bool(args.key):
        print("ERROR! --cert and --key must be used together")
        exit(1)
    if args.verbose or args.debug:
        if SECURE:
            print("Using HTTPS on port %d" % args.port)
        else:
            print("Using HTTP on port %d" % args.port)

    thread = threading.Thread(target=output_reading_thread)
    thread.start()

    if SECURE:
        try:
            context = (args.cert, args.key)
            if args.debug:
                app.run(port=args.port, debug=True, ssl_context=context, host=args.host)
            else:
                app.run(port=args.port, debug=False, ssl_context=context, host=args.host)
        except Exception as e:
            if args.debug:
                print(e)
                exit(2)
            else:
                print("ERROR! Invalid certificate ,key, or host")
                print("Use --debug for more info")
                exit(2)
    else:
        app.run(port=args.port, debug=args.debug, host=args.host)
