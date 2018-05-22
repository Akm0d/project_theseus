// Test sketch for the lid board

#include <Keypad.h>
#include "Adafruit_LEDBackpack.h"

// Pinouts
#define RGB_RED_PIN 13 // D13
#define RGB_GREEN_PIN A0
#define RGB_BLUE_PIN A1
#define BUZZER_PIN 12 // D12

// Macros
#define RGB_RED_ON digitalWrite(RGB_RED_PIN, HIGH);
#define RGB_RED_OFF digitalWrite(RGB_RED_PIN, LOW);
#define RGB_GREEN_ON digitalWrite(RGB_GREEN_PIN, HIGH);
#define RGB_GREEN_OFF digitalWrite(RGB_GREEN_PIN, LOW);
#define RGB_BLUE_ON digitalWrite(RGB_BLUE_PIN, HIGH);
#define RGB_BLUE_OFF digitalWrite(RGB_BLUE_PIN, LOW);

// Keypad 
#define numRows 4 //number of rows on the keypad
#define numCols 4 //number of columns on the keypad

// Seven Segment Display
#define BAUD_RATE 115200

// Global Variables

// Keypad
//keymap defines the key pressed according to the row and columns just as appears on the keypad
char keymap[numRows][numCols]= {
  {'1', '2', '3', 'A'}, 
  {'4', '5', '6', 'B'}, 
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};
//Code that shows the the keypad connections to the arduino terminals
byte rowPins[numRows] = {9,8,7,6}; //Rows 0 to 3
byte colPins[numCols]=  {5,4,3,2}; //Columns 0 to 3
//initializes an instance of the Keypad class

Keypad myKeypad= Keypad(makeKeymap(keymap), rowPins, colPins, numRows, numCols);

// Seven segment display
Adafruit_7segment sevenseg = Adafruit_7segment();

// Function prototypes
void initRgbLedPins();
void testRgbLed();
void initBuzzer();
void testBuzzer();
void initDisplay();
void testDisplay();
void initKeypad();
void testKeypad();

void setup() {
  initRgbLedPins();
  initBuzzer();
  initDisplay();
  initKeypad();
}

void loop() {
//  while(1) {
//    testDisplay();
//    delay(1000);
//  }
  
  #define MAX_I 99
  static int i = MAX_I;

  // Every 100 ms
  if ((i % 10) == 0) {
    char keypressed = myKeypad.getKey();
    if (isdigit(keypressed)) {
      displayNumber(keypressed-'0');
    }
  }
  
  // Every 500 ms
  if ((i % 50 ) == 0) {
    testRgbLed();
  }

  // Every 1 second
  if (i == 0) {
    testBuzzer();
  }

  if (--i < 0) {
    i = MAX_I;
  }
  delay(10);
}

void initDisplay() {
  Serial.begin(BAUD_RATE);
  sevenseg.begin(0x70);
}

void testDisplay() {
  static int i = 0;
  displayNumber(i++);
  if (i > 9) i = 0;
}

void initKeypad() {
  
}

void displayNumber(int number) {
  sevenseg.writeDigitNum(0, number, false);
  sevenseg.writeDisplay();
  
//   sevenseg.writeDigitNum(0,minutes/10,false);
//   sevenseg.writeDigitNum(1,minutes%10,false);
//   sevenseg.drawColon(true);
//   sevenseg.writeDigitNum(3,seconds/10,false);
//   sevenseg.writeDigitNum(4,seconds%10,false);
//   sevenseg.writeDisplay();
}

void testKeypad() {
  char keypressed = myKeypad.getKey();
  if (isdigit(keypressed)) {
    Serial.print("Pressed ");
    Serial.println(keypressed);
  }
}

void initBuzzer() {
  pinMode(BUZZER_PIN, OUTPUT);
}

void testBuzzer() {
//  static boolean i = false;
//  if (i == true) {
//    tone(BUZZER_PIN, 440);
//  }
//  else {
//    tone(BUZZER_PIN, 0);
//  }
//  i = !i;
}

void initRgbLedPins() {
  pinMode(RGB_RED_PIN, OUTPUT);
  pinMode(RGB_BLUE_PIN, OUTPUT);
  pinMode(RGB_GREEN_PIN, OUTPUT);
}

void testRgbLed() {
  static int state = 0;
  switch(state) {
    case 0:
      RGB_BLUE_OFF;
      RGB_RED_ON;
      state++;
      break;
    case 1:
      RGB_RED_OFF;
      RGB_GREEN_ON;
      state++;
      break;
    case 2:
      RGB_GREEN_OFF;
      RGB_BLUE_ON;
      state = 0;
      break;
    default:
      state = 0;
      break;
  }
}

