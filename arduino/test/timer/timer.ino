#include <Wire.h> // Enable this line if using Arduino Uno, Mega, etc.

#include "Adafruit_LEDBackpack.h"
#include "Adafruit_GFX.h"
#include <avr/interrupt.h>

// Macros
#define LED 4 // Digital write to LED on D4
#define SIGNAL 3// The OR'd input from all the other sensors
#define START 2// The multipurpose button for controlling the timer
#define BAUD_RATE 9600
#define MAX_MINUTES 10;
#define MAX_SECONDS 59;
#define SECOND 1000 // One second is 1000 milliseconds
#define TEST 10// Decrement much faster while testing
#define DEBOUNCE 200// Millisecond debounce for switches

#define digitalPinToInterrupt(x) (x - 2)

// Global Variables
Adafruit_7segment sevenseg = Adafruit_7segment();
static int minutes = MAX_MINUTES;
static int seconds = MAX_SECONDS;
static bool running = false;
static bool tripped = false;
static bool start = false;

// Function Prototypes
void reset();
void dead();
void dec_timer();
void buttonInterrupt();

void setup() {
#ifndef __AVR_ATtiny85__
  Serial.begin(BAUD_RATE);
  Serial.println("7 Segment Backpack Test");
#endif
  pinMode(LED,OUTPUT);
  pinMode(START,INPUT_PULLUP);
  pinMode(SIGNAL,INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(START),startInterrupt,RISING);
  attachInterrupt(digitalPinToInterrupt(SIGNAL),buttonInterrupt,RISING);
  sevenseg.begin(0x70);
  reset();
  interrupts();
}

void loop() {
  if (tripped){
    tripped = false;
    dead();
    delay(DEBOUNCE);
  }
  if (start) {
    start = false;
    if (running){
      reset();
    } else {
      running = true;
    }
    delay(DEBOUNCE);
  }
  if (running){
    delay(SECOND);// Change SECOND to TEST for development and testing
    dec_timer();
  }
}

void startInterrupt(){
  start = true;
}
void buttonInterrupt(){
  tripped = true;
}

void drawTime(){
   sevenseg.writeDigitNum(0,minutes/10,false);
   sevenseg.writeDigitNum(1,minutes%10,false);
   sevenseg.drawColon(true);
   sevenseg.writeDigitNum(3,seconds/10,false);
   sevenseg.writeDigitNum(4,seconds%10,false);
   sevenseg.writeDisplay();
}

// Reset the timer to 10 minutes and 0 seconds
void reset(){
   running = false;
   digitalWrite(LED,LOW);
   minutes = MAX_MINUTES;
   seconds = 0;
   drawTime();// Draw the new time
   // Press the START button to start the timer.
}

// Draw the word "dead" on the display until the START button is pressed
// Light up the LED that signifies a death signal
void dead(){
    reset();
    digitalWrite(LED,HIGH);
    sevenseg.drawColon(false);
    // print a hex number
    sevenseg.print(0xDEAD, HEX);
    sevenseg.writeDisplay();
    // This line will hold dead as long as a signal is tripped
    //while(digitalRead(SIGNAL)){}
    //reset();
}

// Decrement the timer until it reaches 0
void dec_timer(){
  if (seconds) seconds--;
  else if (minutes){
    minutes--;
    seconds = MAX_SECONDS;
  } else dead();
  drawTime();
}

