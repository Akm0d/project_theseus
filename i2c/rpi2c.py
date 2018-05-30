#!/usr/bin/env python
#
# RPi2c - test i2c communication between an Arduino and a Raspberry Pi.
#
# Copyright (c) 2013 Carlos Rodrigues <cefrodrigues@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#


from __future__ import division
from __future__ import print_function

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError or ImportError:
    from Adafruit_GPIO import GPIO
import smbus
import sys

I2C_BUS = 1
I2C_SLAVE = 0x1d

INTERRUPT_PIN = 17


def interpolate(value, a1, a2, b1, b2):
    # Normalize the value into a 0..1 interval...
    n = float(value - a1) / float(a2 - a1)

    # Scale the normalized value to the target interval...
    return b1 + (n * (b2 - b1))


if __name__ == '__main__':
    # Initialize the interrupt pin...
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(INTERRUPT_PIN, GPIO.IN)

    # Initialize the RPi I2C bus...
    i2c = smbus.SMBus(I2C_BUS)

    while 1:
        try:
            # Wait until the Arduino triggers the interrupt...
            # GPIO.wait_for_edge(INTERRUPT_PIN, GPIO.RISING)

            try:
                # Get the sensor value from the Arduino (signed 16bit little-endian)...
                sensor_value = i2c.read_word_data(I2C_SLAVE, 0x00)
                sys.stdout.write("sensor: %d" % sensor_value)
            except IOError:
                sys.stderr.write("*** error: receiving sensor value ***\n")
                continue

            sys.stdout.write(" / ")

            try:
                # Map the sensor value to a [0, 255] interval...
                led_value = int(interpolate(sensor_value, 0, 1023, 0, 255))
                sys.stdout.write("led: %d\n" % led_value)

                # Send the PWM value for the LED to the Arduino...
                i2c.write_byte_data(I2C_SLAVE, 0x01, led_value)
            except IOError:
                sys.stderr.write("*** error: sending led value ***\n")

        except KeyboardInterrupt:
            GPIO.cleanup()

# vim: set expandtab ts=4 sw=4:
