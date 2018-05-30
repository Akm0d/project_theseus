#include <Keypad.h>
#include <Wire.h> 
#include "Adafruit_LEDBackpack.h"
#include "Adafruit_GFX.h"
#include <avr/interrupt.h>

/****************Macros*********************/
// Buzzer
#define buzzer 12
#define T_BEEP 10000 // The amount of time to play the beep sound
#define T_ERROR 50000 // The amount of time to play an error sound
#define note(x) (440.0 * pow(2.0,((x)/12.0)))// Algorithm  -21 to 47 are notes on a 66 key piano.-14 is middle c

// Keypad 
#define numRows 4 //number of rows on the keypad
#define numCols 4 //number of columns on the keypad

// Timer
#define TEST 10// Decrement much faster while testing
#define DEBOUNCE 200// Millisecond debounce for switches
#define MAX_MINUTES 3 
#define MAX_SECONDS 59
#define SECOND 50000 // This value may change as the code gets larger, it determines the delay for one second

// RGB
#define RGB_R 13
#define RGB_G 14
#define RGB_B 15


// SERIAL
//outgoing
#define BAUD_RATE 115200
#define ARDUINO_NUMBER '3'
#define RECEIVE 'c'
#define SUCCESS 's'
#define FAILURE 'f'
#define HEARTBEAT 'h'
#define ALIVE 'a'
#define KEYPRESS 'k'
#define TICK 'T'
//incoming
#define START_TIMER 't'
#define UPDATE_RGB 'u'
#define RGB_BLUE 'B'
#define RGB_RED 'R'
#define RGB_GREEN 'G'
#define RGB_OFF 'O'
#define DEAD 'd'
#define RESET 'r'
#define NO_MESSAGE -1
// Timing
#define RECEIVE_MAX SECOND / 200
// The rate for sending heartbeats
// It has to be frequent, but no so often that it drowns out other signals
#define KEEP_ALIVE_MAX SECOND * 2

/********************************************/

/************Global Variables****************/
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

// Timer
Adafruit_7segment sevenseg = Adafruit_7segment();
static int minutes = MAX_MINUTES;
static int seconds = MAX_SECONDS;
static bool running = false;
static bool tripped = false;
static bool start = false;

// Delay timers
static unsigned int t_debounce = 0;
static unsigned int t_receive = 0;
static long unsigned int t_buzz = 0;
static long unsigned int t_heartbeat = 0;

// Serial
char data = NO_MESSAGE;
char mesg_code = NO_MESSAGE;
/********************************************/


/***********Function Prototypes**************/
//Keypad
void play_keyTone(char keypressed);

// Timer
void reset();
void dead();
void dec_timer();
void buttonInterrupt();

// Arduino
void dec_timers();

//Serial
void receive_mesg();
void send_mesg(char code, char data);
/********************************************/

void setup(){
  pinMode(buzzer,OUTPUT);
  Serial.begin(BAUD_RATE);
  sevenseg.begin(0x70);
  reset();
  interrupts();

}

void loop(){
  if(!t_heartbeat){
    t_heartbeat = KEEP_ALIVE_MAX;
    send_mesg(HEARTBEAT,ALIVE);
  }
  char keypressed = myKeypad.getKey();
  if (keypressed != NO_KEY) {
    //Serial.print(keypressed);
    play_keyTone(keypressed);
  }
  if (tripped){
    tripped = false;
    dead();
    t_debounce = DEBOUNCE;
  }
  if (start) {
    start = false;
    if (running){
      reset();
    } else {
      running = true;
    }
    t_debounce = DEBOUNCE;
  }

  dec_timers();
  receive_mesg();
}

void receive_mesg(){
  //listen for incoming command data
  // Receive the message code if none has been given
  if(Serial.available() && mesg_code == NO_MESSAGE){
    mesg_code = Serial.read();
    t_receive = RECEIVE_MAX;
  } else if(Serial.available() && !t_receive && data == NO_MESSAGE){
    data = Serial.read();
    
  } else if(!t_receive && !(data == NO_MESSAGE) && !(mesg_code == NO_MESSAGE)){
    //check for message codes and execute command
    switch (mesg_code){
      case START_TIMER:
        startInterrupt();
        send_mesg(START_TIMER,SUCCESS);
        break;
      case DEAD:
        buttonInterrupt();
        send_mesg(DEAD,SUCCESS);
        break;
      case RESET:
        reset();
        send_mesg(RESET,SUCCESS);
        break;
      case RGB_GREEN:
        digitalWrite(RGB_R,LOW);
        digitalWrite(RGB_G,HIGH);
        digitalWrite(RGB_B,LOW);
        send_mesg(UPDATE_RGB,SUCCESS);
        break;
      case RGB_BLUE:
        digitalWrite(RGB_R,LOW);
        digitalWrite(RGB_G,LOW);
        digitalWrite(RGB_B,HIGH);
        send_mesg(UPDATE_RGB,SUCCESS);
        break;
      case RGB_RED:
        digitalWrite(RGB_R,HIGH);
        digitalWrite(RGB_G,LOW);
        digitalWrite(RGB_B,LOW);
        send_mesg(UPDATE_RGB,SUCCESS);
        break;
      case RGB_OFF:
        digitalWrite(RGB_R,LOW);
        digitalWrite(RGB_G,LOW);
        digitalWrite(RGB_B,LOW);
        send_mesg(UPDATE_RGB,SUCCESS);
        break;
      case TICK:
        if(running){
          dec_timer();
          send_mesg(TICK, SUCCESS);
        } else {
          send_mesg(TICK, FAILURE);
        }
        break;
      default:
        send_mesg(RECEIVE,mesg_code);
        break;
    }
    // After handling data, reset the message code
    mesg_code = NO_MESSAGE;// Reset message code
    data = NO_MESSAGE;
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
   //digitalWrite(LED,LOW);
   minutes = MAX_MINUTES;
   seconds = 0;
   drawTime();// Draw the new time
   // Press the START button to start the timer.
}

// Draw the word "dead" on the display until the START button is pressed
// Light up the LED that signifies a death signal
void dead(){
    reset();
    //digitalWrite(LED,HIGH);
    sevenseg.drawColon(false);
    // print a hex number
    sevenseg.print(0xDEAD, HEX);
    sevenseg.writeDisplay();
    // This line will hold dead as long as a signal is tripped
    //while(digitalRead(SIGNAL)){}
    //reset();
    play_keyTone('x');
}

// Decrement the timer until it reaches 0
void dec_timer(){
  if (seconds) seconds--;
  else if (minutes){
    minutes--;
    seconds = MAX_SECONDS;
  } else {
    dead();
    return;
  }
  drawTime();
}

void play_keyTone(char keypressed){
   switch(keypressed){
      case '0':
        tone(buzzer,note(-14));
        break;
      case '1':
        tone(buzzer,note(-13));
        break;
      case'2':
        tone(buzzer,note(-12));
        break;
      case'3':
        tone(buzzer,note(-11));
        break;
      case '4':
        tone(buzzer,note(-10));
        break;
      case '5':
        tone(buzzer,note(-9));
        break;
      case '6':
        tone(buzzer,note(-8));
        break;
      case '7':
        tone(buzzer,note(-7));
        break;
      case '8':
        tone(buzzer,note(-6));
        break;
      case '9':
        tone(buzzer,note(-5));
        break;
      case 'A':
        tone(buzzer,note(-4));
        break;
      case 'B':
        tone(buzzer,note(-3));
        break;
      case 'C':
        tone(buzzer,note(-2));
        break;
      case 'D':
        tone(buzzer,note(-1));
        break;      case 'E':
        tone(buzzer,note(-0));
        break;
      case '*':
        keypressed = 'E';
        tone(buzzer,note(1));
        break;
      case '#':
        keypressed = 'F';
        tone(buzzer,note(2));
        break;
      default:
        tone(buzzer,note(-30));
        t_buzz = T_ERROR;
        break;
    }
    send_mesg(KEYPRESS,keypressed);

    // Play the sound for (100 milliseconds)
    if (!t_buzz) t_buzz = T_BEEP;

}


// Decrements all delay timers
void dec_timers(){
  if (t_buzz) t_buzz--;
  else noTone(buzzer); //Stop playing sounds if buzzer timer is zero
  if (t_debounce) t_debounce--;
  if (t_receive) t_receive--;
  if (t_heartbeat) t_heartbeat--;
}

void send_mesg(char code,char data){
  Serial.print(ARDUINO_NUMBER);
  Serial.print(" ");
  Serial.print(code);
  Serial.print(" ");
  Serial.println(data);
}

