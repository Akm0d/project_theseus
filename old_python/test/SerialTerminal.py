#!/usr/bin/env python3
import sys, tty, termios, select
import serial
import glob
import time
import array

# If you haven't implemented watchdog timers then leave this as false
# TODO change this variable with a command line switch
setWatchdog(False)

help_text = "\
[1-9] Send data to arduino number\n\
c     connect to all arduinos\n\
d     disconnect from all arduinos\n\
h     show this help text\n\
l     list possible connections\n\
r     reset all arduino connections\n\
q     quit this program\n\
"


# A class to hold an arduino number and serial connection together
class Arduino:
    def __init__(self, serial, port):
        self.serial = serial
        self.port = port
        self.number = None
        self.watchdog_timer = 0
        self.watchdog_timeout = 5000
        # Get the number of the arduino from its heartbeat
        data = self.serial.readline()
        print("finding arduino number")
        try:
            data = self.serial.readline()
            while not data:
                data = self.serial.readline()
            # read data twice so that we get a full message
            data = self.serial.readline()
            while not data:
                data = self.serial.readline()
            self.number = int(data.decode("utf-8")[0])
            print("Arduino number %d found on %s" % (self.number, port))
        except Exception as e:
            print("Communication error while finding number")

    def reset_watchdog_timer(self):
        # print("Resetting watchdog timer from %s"%self.watchdog_timer)
        self.watchdog_timer = 0

    def increment_watchdog_timer(self):
        if getWatchdog() and self.number:
            self.watchdog_timer += 1
            if self.watchdog_timer >= self.watchdog_timeout:
                print("Watchdog timer expired on arduino %s" % self.number)
                game_over = True


class Getch(object):
    def __enter__(self):
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        return self

    def __exit__(self, type, value, traceback):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def get_data(self):
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            char = sys.stdin.read(1)
            # print(char)
            return char
        return False


def scan_ports():
    return glob.glob('/dev/ttyUSB*')


class Test:
    def __init__(self):
        self.baud_rate = "115200"
        self.serial_ports = scan_ports()
        self.arduinos = {}
        for port in self.serial_ports:
            print("Connecting to device on %s" % port)
            self.arduinos[port] = Arduino(serial.Serial(port, self.baud_rate, timeout=0), port)
        self.cmd = 's'

    def reset(self):
        self.disconnect()
        self.arduinos = {}
        self.connect()

    def disconnect(self):
        for port in self.arduinos:
            if self.arduinos[port].serial.is_open:
                self.arduinos[port].serial.close()
            else:
                print("No connection is open on port %s" % port)

    def connect(self):
        self.serial_ports = scan_ports()
        for port in self.serial_ports:
            print("Connecting to device on %s" % port)
            try:
                self.arduinos[port] = Arduino(serial.Serial(port, self.baud_rate, timeout=0), port)
            except Exception as e:
                print("Couldn't find a device on port %s" % port)

    # Return an arduino object for the specified arduino number
    def arduino(self, number):
        for port in self.arduinos:
            if self.arduinos[port].number == number:
                return self.arduinos[port]
        print("arduino %s not found"% number)
        return None

    @property
    def run(self):
        print(help_text)
        with Getch() as getch:
            while True:
                key = getch.get_data()
                if key == 'q':
                    print("Exiting")
                    return 0
                elif key == 'r':
                    print("Resetting Connection")
                    self.reset()
                elif key == 'd':
                    print("Disconnecting from device")
                    self.disconnect()
                elif key == 'c':
                    print("Connecting to device")
                    self.connect()
                elif key == 'h':
                    print(help_text)
                elif key == 'l':
                    self.list_devices()
                else:
                    serial = None
                    number = None
                    # choose arduino that will receive data
                    try:
                        number = int(key)
                    except Exception as e:
                        do_nothing = True
                    if number:
                        print(number)
                        for port in self.arduinos:
                            if self.arduinos[port].number == number:
                                serial = self.arduinos[port].serial
                                if not serial.is_open:
                                    print("Arduino is not connected on port %s" % port)
                        if not serial:
                            print("Arduino number %s not found" % number)
                        else:
                            self.cmd = input("Send a command: ")
                            try:
                                serial.write(array.array('B', self.cmd.encode('utf-8')))
                                print(self.cmd)
                            except Exception as e:
                                print("You inputted an invalid string")
                                print("String format: <XY Z> where XY and Z are of the format '0xBEEF'")
                    else:  # if a number wasn't the command, then just receive data and increment watchdog timers
                        for port in self.arduinos:
                            if self.arduinos[port].serial.is_open:
                                # Get data from device and parse it
                                self.arduinos[port].increment_watchdog_timer()
                                try:
                                    data = self.arduinos[port].serial.readline()
                                    if data:
                                        self.parse(data)
                                except Exception as e:
                                    print ("Arduino %s disconnected unexpectedly" % self.arduinos[port].number)
                                    self.reset()

    def parse(self, byte_data):
        arduino_number = 0
        message = byte_data.decode().split(' ')
        try:
            arduino_number = message[0][0]
            information_type = message[1][0]
            data = message[2][0]
        except Exception as e:
            print("Message from arduino %s didn't have enough arguments" % arduino_number)
            return
        if arduino_number == '1':
            # Code for receiving message from arduino 1
            do_thing = True
        elif arduino_number == '2':
            # Code for receiving message from arduino 2
            do_thing = True
        elif arduino_number == '3':
            # Code for receiving message from arduino 3
            if information_type == 'h':
                if data == 'a':
                    # the heartbeat timer increments constantly, and is reset by heartbeats
                    # it is kept in the Arduino class, and if it expires, this script
                    # sends arduino 3 the "dead" signal
                    self.arduino(int(arduino_number)).reset_watchdog_timer()
            elif information_type == 'd':
                if data == "s":
                    print("0xdead signal successfully sent")
                else:
                    print("0xdead signal encountered error")
            elif information_type == 'k':
                print("Touchpad sent %s" % data)
            elif information_type == 'c':
                print("Arduino received bad message code '%s'" % data)
            elif information_type == 'l':
                if data == 's':
                    print("update rgb was successful")
                else:
                    print("update rgb encountered an error")
            elif information_type == 't':
                if data == 's':
                    print("start timer was successful")
                else:
                    print("start timer encountered an error")
            elif information_type == 'u':
                if data == "s":
                    print("RGB update successful")
                else:
                    print("RGB update encountered an error")
            elif information_type == 'r':
                if data == 's':
                    print("Timer reset was successful")
                else:
                    print("Timer reset encountered an error")
            else:
                print("Unrecognized information type '%s' for arduino %s" % (information_type, arduino_number))
        else:
            print("Unrecognized Arduino number %s" % arduino_number)

    # Lists out the arduino connections
    def list_devices(self):
        for port in self.arduinos:
            if self.arduinos[port].serial.is_open: print("Arduino %s connected on %s" % (self.arduinos[port].number, self.arduinos[port].port))
            else:
                print("Arduino %s suspended on %s" % (self.arduinos[port].number, self.arduinos[port].port))


a = Test()
a.run
