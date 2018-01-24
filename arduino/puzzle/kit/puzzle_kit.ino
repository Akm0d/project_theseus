#include <Keypad.h>
#include <Wire.h> 

/****************Macros*********************/
// Timer
#define SECOND 99166 // This value may change as the code gets larger, it determines the delay for one second
#define DEBOUNCE_MAX 2000

// SERIAL
//outgoing
#define ARDUINO_NUMBER '2'
#define RECEIVE 'c'
#define SUCCESS 's'
#define FAILURE 'f'
#define HEARTBEAT 'h'
#define ALIVE 'a'
#define SWITCH_VALUE 'w'
#define POT_VALUE 'p'
#define DEAD_ZONE 'Z'
#define RED_WIRE_M 'R'
#define BLUE_WIRE_M 'B'
//incoming
#define LOCK 'l'
#define UNLOCK 'u'
#define CORRECT 'c'
#define INCORRECT 'o'

#define NO_MESSAGE -1
// Timing
#define RECEIVE_MAX SECOND / 200
// The rate for sending heartbeats
// It has to be frequent, but no so often that it drowns out other signals
#define KEEP_ALIVE_MAX SECOND / 2

// Test sketch for suitcase board
// Author(s): Marshall Garey

// Pinouts:
#define LED0_PIN 2 // D2
#define LED1_PIN 3 // D3
#define LED2_PIN 4 // D5
#define LED3_PIN 5 // D5
#define LED4_PIN 6 // D6
#define LED5_PIN 7 // D7
#define LED6_PIN 8 // D8
#define LED7_PIN 9 // D9
#define RED_WIRE_PIN 18 // A4
#define BLUE_WIRE_PIN 19 // A5
#define POT_PIN A2 // A2
#define SW0_PIN 12 // D12
#define SW1_PIN 14 // D14
#define SW2_PIN 10 // D10
#define SW3_PIN 15 // A0
#define SW4_PIN 11 // A1
#define FAN_PIN 13 // D13
#define SOLENOID_PIN A3 // A3

#define BAUD_RATE 115200

#define CORRECT_SIG LED0_PIN

/********************************************/

/************Global Variables****************/
int last_data = 0;
char last_pot;

// Delay timers
static unsigned int t_debounce = 0;
static unsigned int t_receive = 0;
static long unsigned int t_heartbeat = 0;

// Serial
char data = NO_MESSAGE;
char mesg_code = NO_MESSAGE;
/********************************************/


/***********Function Prototypes**************/

// Timer
void switchInterrupt();

//Serial
void receive_mesg();
void send_mesg(char code, char data);
void read_sensors();
void read_pot();
void testRedBlue();
/********************************************/

void setup(){
  pinMode(LED0_PIN, OUTPUT);
  pinMode(LED1_PIN, OUTPUT);
  pinMode(LED2_PIN, OUTPUT);
  pinMode(LED3_PIN, OUTPUT);
  pinMode(LED4_PIN, OUTPUT);
  pinMode(LED5_PIN, OUTPUT);
  pinMode(LED6_PIN, OUTPUT);
  pinMode(LED7_PIN, OUTPUT);
  pinMode(FAN_PIN, OUTPUT);
  pinMode(SOLENOID_PIN, OUTPUT);
  pinMode(RED_WIRE_PIN, INPUT);
  pinMode(BLUE_WIRE_PIN, INPUT);
  pinMode(SW0_PIN, INPUT);
  pinMode(SW1_PIN, INPUT);
  pinMode(SW2_PIN, INPUT);
  pinMode(SW3_PIN, INPUT);
  pinMode(SW4_PIN, INPUT);
  digitalWrite(FAN_PIN, HIGH);
  Serial.begin(BAUD_RATE);
}

void loop(){
  if(!t_heartbeat){
    t_heartbeat = KEEP_ALIVE_MAX;
    send_mesg(HEARTBEAT,ALIVE);
  }
  receive_mesg();
  dec_timers();
  read_sensors();
  if(!t_debounce){
    read_pot();
    t_debounce = DEBOUNCE_MAX;
  }
  testRedBlue();
}

void testRedBlue(){
  // Test red wire
  static int redWireState = HIGH;

  int redWire = digitalRead(RED_WIRE_PIN);
  switch(redWireState) {
    case HIGH:
      if (!redWire) {
        redWireState = LOW;
        send_mesg(RED_WIRE_M, RED_WIRE_M);
      }
      break;
    case LOW:
      if (redWire) {
        redWireState = HIGH;
      }
      break;
    default:
      redWireState = HIGH;
      break;
  }

  // Test blue wire. Same as red wire. I could code this so it's not duplicate code, but I'm lazy.
  static int blueWireState = HIGH;
  int blueWire = digitalRead(BLUE_WIRE_PIN);
  switch(blueWireState) {
    case HIGH:
      if (!blueWire) {
        blueWireState = LOW;
        send_mesg(BLUE_WIRE_M, BLUE_WIRE_M);
       }
      break;
    case LOW:
      if (blueWire) {
        blueWireState = HIGH;
      }
      break;
    default:
      blueWireState = HIGH;
      break;
  }
}

void read_pot(){
  int res = analogRead(POT_PIN) / 10;
  char new_pot;
  if (res >= 102){
    digitalWrite(LED7_PIN, LOW);
    digitalWrite(LED6_PIN, LOW);
    digitalWrite(LED5_PIN, LOW);
    new_pot = DEAD_ZONE;
  } else if (res >= 85){
    digitalWrite(LED7_PIN, HIGH);
    digitalWrite(LED6_PIN, LOW);
    digitalWrite(LED5_PIN, LOW);
    new_pot = '0';
  } else if (res >= 30){
    digitalWrite(LED7_PIN, LOW);
    digitalWrite(LED6_PIN, HIGH);
    digitalWrite(LED5_PIN, LOW);
    new_pot = '1';
  } else if (res >= 0){
    digitalWrite(LED7_PIN, LOW);
    digitalWrite(LED6_PIN, LOW);
    digitalWrite(LED5_PIN, HIGH);
    new_pot = '2';
  }
  if (new_pot != last_pot){
    last_pot = new_pot;
    send_mesg(POT_VALUE, new_pot);
  }
}

void read_sensors(){
  int sw = digitalRead(SW0_PIN);
  int sensor_data = sw;
  sensor_data <<= 1;
  sw = digitalRead(SW1_PIN);
  digitalWrite(LED4_PIN, sw? HIGH:LOW);
  sensor_data |= sw;
  sensor_data <<= 1;
  sw = digitalRead(SW2_PIN);
  digitalWrite(LED3_PIN, sw? HIGH:LOW);
  sensor_data |= sw;
  sensor_data <<= 1;
  sw = digitalRead(SW3_PIN);
  digitalWrite(LED2_PIN, sw? HIGH:LOW);
  sensor_data |= sw;
  sensor_data <<= 1;
  sw = digitalRead(SW4_PIN);
  digitalWrite(LED1_PIN, sw? HIGH:LOW);
  sensor_data |= sw;
  if (sensor_data != last_data){
    last_data = sensor_data;
    send_mesg(SWITCH_VALUE, sensor_data + 'A');
  }
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
      case CORRECT:
        digitalWrite(CORRECT_SIG,HIGH);
        send_mesg(CORRECT,SUCCESS);
        break;
      case INCORRECT:
        digitalWrite(CORRECT_SIG,LOW);
        send_mesg(INCORRECT,SUCCESS);
        break;
      case LOCK:
        digitalWrite(SOLENOID_PIN, LOW);
        send_mesg(LOCK,SUCCESS);
        break;
      case UNLOCK:
        digitalWrite(SOLENOID_PIN, HIGH);
        send_mesg(UNLOCK,SUCCESS);
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

// Decrements all delay timers
void dec_timers(){
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
