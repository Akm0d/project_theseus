/*
 * RPi2c - test i2c communication between an Arduino and a Raspberry Pi.
 *
 * Copyright (c) 2013 Carlos Rodrigues <cefrodrigues@gmail.com>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */


#include <Wire.h>


static const char intPin = 8;
static const char ledPin = 9;
static const char sensorPin = A0;

short ledValue = 0;
short sensorCurr = 0;
short sensorPrev = -10;


void setup()
{
  pinMode(intPin, OUTPUT);
  pinMode(ledPin, OUTPUT);
  
  Wire.begin(0x03);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
}


void loop() {
  sensorCurr = 0;  
  
  // Take a few samples and average the results to avoid jitter...
  for (int i = 0; i < 10; i++) {
    sensorCurr += analogRead(sensorPin);
    delay(1);
  }
  
  sensorCurr /= 10;

  // Trigger an interrupt on the RPi when the sensor changes...
  if (abs(sensorCurr - sensorPrev) > 1) {
    sensorPrev = sensorCurr;
    
    digitalWrite(intPin, HIGH);
    delay(10);
    digitalWrite(intPin, LOW);
  }
}


void receiveEvent(int bytes) {
  int operation = Wire.read();
  
  // Change the LED intensity...
  if (operation == 0x01 && bytes > 1) {
    ledValue = Wire.read();
    analogWrite(ledPin, ledValue);
  }

  // Consume any remainder bytes...
  while (Wire.available()) {
    Wire.read();
  }
}


void requestEvent() {
  // Both the Arduino and RPi are little-endian, no conversion needed...
  Wire.write((uint8_t *)&sensorCurr, sizeof(sensorCurr));
}


/* EOF - RPi2c.pde */
