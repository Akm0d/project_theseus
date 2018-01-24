#!/usr/bin/env python3
from static.constants import *
import array
import glob
import serial
from functions.keypad import Keypad
from globalVariables import *


# TODO all messages need to be stored in constant strings, that way I can easily act on them

class Arduino:
    """
    A class to combine an arduino number and a serial connection
    Contains a method for resetting each arduino's watchdog timer
    """

    def __init__(self, serial, port):
        global output
        self.serial = serial
        self.port = port
        self.number = None
        self.watchdog_timer = 0
        self.watchdog_timeout = 5000
        # Get the number of the arduino from its heartbeat
        data = self.serial.readline()
        if getDebug() & INFO:
            output.append("finding arduino number")
        try:
            data = self.serial.readline()
            while not data:
                data = self.serial.readline()
            # read data twice so that we get a full message
            data = self.serial.readline()
            while not data:
                data = self.serial.readline()
            self.number = int(data.decode("utf-8")[0])
            if getDebug() & INFO: output.append("Arduino number %d found on %s" % (self.number, port))
        except Exception as e:
            print(e)
            if getDebug() & WARN: output.append("Communication error while finding number")
            if getDebug() & WARN: output.append(str(e))
        pass

    def reset_watchdog_timer(self):
        """
        Reset this arduino's watchdog timer
        """
        # output.append("Resetting watchdog timer from %s"%self.watchdog_timer)
        self.watchdog_timer = 0
        pass

    def increment_watchdog_timer(self):
        """
        Increment this arduino's watchdog timer
        """
        if getWatchdog() and self.number:
            self.watchdog_timer += 1
            if self.watchdog_timer >= self.watchdog_timeout:
                if getDebug() & ERROR: output.append("Watchdog timer expired on arduino %s" % self.number)
                game_over = True
        pass


def get_output():
    """
    Clear output and pass it to the server
    :return: serial data
    """
    global output
    temp = []
    temp.extend(output)
    output.clear()
    return temp


def scan_ports():
    """
    :return: the ttyUSB ports that have active connections
    """
    return glob.glob('/dev/ttyUSB*')


class ArduinoSerial:
    """
    A class that handles connections to each of the arduinos
    """
    global output

    def __init__(self):
        """
        Declare all variables required to communicate with the ArduinoSerial class
        """
        if getDebug() & INFO: output.append("Initializing Arduino Serial Connnections")
        self.baud_rate = "115200"
        self.serial_ports = scan_ports()
        self.arduinos = {}
        for port in self.serial_ports:
            if getDebug() & INFO: output.append("Connecting to device on %s" % port)
            self.arduinos[port] = Arduino(serial.Serial(port, self.baud_rate, timeout=0), port)
        self.cmd = SUCCESS
        pass

    def reset(self):
        """
        disconnect from all arduinos
        delete the list of connections
        scan ports and reconnect to devices
        return a list of connections to the server
        """
        if getDebug() & INFO: output.append("Resetting all connections")
        self.disconnect()
        self.arduinos = {}
        self.connect()
        self.list_devices()
        pass

    def disconnect(self):
        """
        Close serial connections on all arduinos
        """
        for port in self.arduinos:
            if self.arduinos[port].serial.is_open:
                self.arduinos[port].serial.close()
            else:
                if getDebug() & ERROR: output.append("No connection is open on port %s" % port)
        pass

    def connect(self):
        """
        Connect to arduinos on all active ttyUSB ports
        """
        self.serial_ports = scan_ports()
        for port in self.serial_ports:
            if getDebug() & INFO: output.append("Connecting to device on %s" % port)
            try:
                self.arduinos[port] = Arduino(serial.Serial(port, self.baud_rate, timeout=0), port)
            except Exception as e:
                print(e)
                if getDebug() & ERROR: output.append("Couldn't find a device on port %s" % port)
                if getDebug() & ERROR: output.append(str(e))
        pass

    def arduino(self, number):
        """
        :param number: The arduino number that this script recognizes
        :return: a connection to the specified arduino or None
        """
        for port in self.arduinos:
            if self.arduinos[port].number == number:
                return self.arduinos[port]
        if getDebug() & WARN: output.append("arduino %s not found" % number)
        return None

    def send_data(self, number, command):
        """
        :param number: The arduino number
        :param command: the first character to send the arduino
        :param data: the information associated with that character
        """
        if len(command) > 1:
            data = command[1:]  # Data is everything but the first character
            command = command[:1]  # command is the first character
        serial = None
        for port in self.arduinos:
            if self.arduinos[port].number == number:
                serial = self.arduinos[port].serial
                if not serial.is_open:
                    if getDebug() & ERROR: output.append("Arduino is not connected on port %s" % port)
        if serial is None:
            if getDebug() & WARN: output.append("Arduino number %s not found" % number)
        else:
            self.cmd = command + "\n"
            try:
                serial.write(array.array('B', self.cmd.encode('utf-8')))
                # TODO only do this if getDebug() level is high
                # output.append("sent: " + self.cmd + " To arduino " + str(number))
            except Exception as e:
                if getDebug() & ERROR: output.append("You input an invalid string")
                if getDebug() & ERROR: output.append("String format: <XY Z> where XY and Z are of the format '0xBEEF'")
                if getDebug() & ERROR: output.append(str(e))
                print(e)
        pass

    def receive_data(self):
        """
        Retrieve information sent from the arduinos.
        This function should be called regularly by the server
        """
        for port in self.arduinos:
            if self.arduinos[port].serial.is_open:
                # Get data from device and parse it
                self.arduinos[port].increment_watchdog_timer()
                try:
                    data = self.arduinos[port].serial.readline()
                    if data:
                        self.parse(data)
                except Exception as e:
                    if getDebug() & ERROR: output.append("Arduino %s disconnected unexpectedly" % self.arduinos[port].number)
                    if getDebug() & ERROR: output.append(str(e))
                    print(e)
                    self.reset()
        pass

    def parse(self, byte_data):
        """
        Parse the data that came from the arduino
        Send information back to arduinos based on information received
        :param byte_data: The information that came from the arduino
        """
        arduino_number = 0
        message = byte_data.decode().split()
        try:
            arduino_number = message[0][0]
            information_type = message[1][0]
            data = message[2]
        except Exception as e:
            if getDebug() & WARN: output.append("Message from arduino %s didn't have enough arguments" % arduino_number)
            print(e)
            return
        if arduino_number == '1':
            if information_type == HEARTBEAT:
                if data == ALIVE:
                    # the heartbeat timer increments constantly, and is reset by heartbeats
                    # it is kept in the Arduino class, and if it expires, this script
                    # sends arduino 3 the "dead" signal
                    self.arduino(int(arduino_number)).reset_watchdog_timer()
            if information_type == KNOCK_KIT_ULTRASONIC_TRIP:
                if get_timer_running():
                    if get_ultrasonic():
                        if getDebug() & EVENTS: output.append("Ultrasonic was tripped")
                        set_dead(True)
        elif arduino_number == '2':
            if information_type == HEARTBEAT:
                if data == ALIVE:
                    # the heartbeat timer increments constantly, and is reset by heartbeats
                    # it is kept in the Arduino class, and if it expires, this script
                    # sends arduino 3 the "dead" signal
                    self.arduino(int(arduino_number)).reset_watchdog_timer()
            elif information_type == PUZZLE_KIT_CORRECT:
                if data == SUCCESS:
                    if getDebug() & EVENTS: output.append("Signaling correct configuration of switches")
                else:
                    if getDebug() & EVENTS: output.append("Error signalling correct switches")
            elif information_type == PUZZLE_KIT_RED_WIRE:
                set_wire_value(data)
            elif information_type == PUZZLE_KIT_BLUE_WIRE:
                set_wire_value(data)
            elif information_type == PUZZLE_KIT_POT_VALUE:
                if get_timer_running():
                    if data == PUZZLE_KIT_DEAD_ZONE:
                        set_dead(True)
                        if getDebug() & EVENTS: output.append("POT hit the dead zone")
                    else:
                        if getDebug() & EVENTS: output.append("POT is in position %s" % data)
                        set_pot_value(int(data))
            elif information_type == PUZZLE_KIT_CORRECT_OFF:
                if data == SUCCESS:
                    pass
                    #output.append("Signaling incorrect configuration of switches")
                else:
                    if getDebug() & ERROR: output.append("Error signalling incorrect switches")
            elif information_type == PUZZLE_KIT_LOCK:
                if data == SUCCESS:
                    if getDebug() & EVENTS: output.append("Locking the Solenoid")
                else:
                    if getDebug() & ERROR: output.append("Error locking the solenoid")
            elif information_type == PUZZLE_KIT_SWITCH_VALUE:
                set_switches_char(data)
                if getDebug() & EVENTS: output.append("Switches reported '%s'" % data)
            elif information_type == PUZZLE_KIT_UNLOCK:
                # Name of touchpad queue touchpad_input
                if (data == SUCCESS):
                    if getDebug() & EVENTS: output.append("Unlocking the Solenoid")
                else:
                    if getDebug() & ERROR: output.append("Error while unlocking the solenoid")
            elif information_type == PUZZLE_KIT_RANDOMIZE:
                keypadSetCombo(data)
                if getDebug() & EVENTS: output.append("New keypad code is 0x%s" % keypadSprintCombo())
            else:
                if getDebug() & WARN: output.append("Unrecognized information type '%s' for arduino %s" % (information_type, arduino_number))
        elif arduino_number == '3':
            if information_type == HEARTBEAT:
                if data == ALIVE:
                    # the heartbeat timer increments constantly, and is reset by heartbeats
                    # it is kept in the Arduino class, and if it expires, this script
                    # sends arduino 3 the "dead" signal
                    self.arduino(int(arduino_number)).reset_watchdog_timer()
            elif information_type == LID_KIT_TIMER_DEAD:
                if data == SUCCESS:
                    if getDebug() & INFO: output.append("0xdead signal successfully sent")
                else:
                    if getDebug() & ERROR: output.append("0xdead signal encountered error")
            elif information_type == LID_KIT_KEYPRESS:
                if getDebug() & EVENTS: output.append("Touchpad sent %s" % data)
                # It will do nothing if the queue is not big enouph yet
                # Add the pressed key to the touchpad_input queue
                if get_timer_running() and not data == 'x':
                    append_touchpad_input(data)
                    if keypadCheckCombo(getObject_touchpad_input()):
                        # Puzzle complete, they typed the right code
                        print("SUCCESS, OPEN THE SOLINOID")
                        self.send_data(PUZZLE_KIT, PUZZLE_KIT_UNLOCK)
                    else:
                        if getLen_touchpad_input() >= 3:
                            set_dead(True)
                            clear_touchpad_input()
            elif information_type == RECEIVE:
                if getDebug() & WARN: output.append("Arduino received bad message code '%s'" % data)
            elif information_type == 'u':
                if data == SUCCESS:
                    if getDebug() & EVENTS: output.append("update rgb was successful")
                else:
                    if getDebug() & ERROR: output.append("update rgb encountered an error")
            elif information_type == LID_KIT_TIMER_START:
                if data == SUCCESS:
                    if getDebug() & EVENTS: output.append("start timer was successful")
                else:
                    if getDebug() & ERROR: output.append("start timer encountered an error")
            elif information_type == LID_KIT_TIMER_RESET:
                if data == SUCCESS:
                    if getDebug() & EVENTS: output.append("Timer reset was successful")
                else:
                    if getDebug() & ERROR: output.append("Timer reset encountered an error")
            elif information_type == LID_KIT_TICK:
                # TODO Do something with the tick
                pass
            else:
                if getDebug() & WARN: output.append("Unrecognized information type '%s' for arduino %s" % (information_type, arduino_number))
        elif arduino_number == '4':
            if information_type == HEARTBEAT:
                if data == ALIVE:
                    # the heartbeat timer increments constantly, and is reset by heartbeats
                    # it is kept in the Arduino class, and if it expires, this script
                    # sends arduino 3 the "dead" signal
                    self.arduino(int(arduino_number)).reset_watchdog_timer()
            elif information_type == LED_KIT_TRIPPED:
                if get_timer_running():
                    set_dead(True)
                    if getDebug() & EVENTS: output.append("Laser tripwire %s was triggered" % data)
            else:
                if getDebug() & WARN: output.append("Unrecognized information type '%s' for arduino %s" % (information_type, arduino_number))
        else:
            if getDebug() & WARN: output.append("Unrecognized Arduino number %s" % arduino_number)
        pass

    # Lists out the arduino connections
    def list_devices(self):
        """
        Send the server a list of the connected arduinos and their tty port
        """
        if self.arduinos:
            for port in self.arduinos:
                if self.arduinos[port].serial.is_open:
                    if getDebug() & INFO: output.append("Arduino %s connected on %s" % (self.arduinos[port].number, self.arduinos[port].port))
                else:
                    if getDebug() & INFO: output.append("Arduino %s suspended on %s" % (self.arduinos[port].number, self.arduinos[port].port))
        else:
            if getDebug(): output.append("No arduinos found")
        pass


if __name__ == "__main__":
    """
    Deprecated, do not use
    """
    a = ArduinoSerial()
    a.run
