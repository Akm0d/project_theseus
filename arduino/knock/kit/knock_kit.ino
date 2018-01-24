#include <Arduino.h>

#define TriggerPin 11
#define EchoPin 10

// Serial
#define SECOND 100 // This value may change as the code gets larger, it determines the delay for one second
#define BAUD_RATE 115200
#define ARDUINO_NUMBER '1'
#define RECEIVE 'c'
#define SUCCESS 's'
#define FAILURE 'f'
#define HEARTBEAT 'h'
#define ALIVE 'a'
#define ULTRASONIC_TRIP 'u'
//incoming
#define NO_MESSAGE -1

// Timing
#define RECEIVE_MAX SECOND / 200
// The rate for sending heartbeats
// It has to be frequent, but no so often that it drowns out other signals
#define KEEP_ALIVE_MAX SECOND * 2

#define ULTRASONIC_LOW 180
#define ULTRASONIC_HIGH 220
#define TRIP_MAX 1000

/********************************************/
// Delay timers
static unsigned int t_receive = 0;
static long unsigned int t_heartbeat = 0;

// Serial
char data = NO_MESSAGE;
char mesg_code = NO_MESSAGE;
bool tripped = false;
int trip_count = 0;

/***********Function Prototypes**************/
//Arduino 
void dec_timers();
long getDistance(long);
void receive_mesg();
void send_mesg(char code, char data);

void setup(){
  pinMode(TriggerPin,OUTPUT); // Trigger is an output pin
  pinMode(EchoPin,INPUT); // Echo is an input pin 
  Serial.begin(115200); // Serial Output
}

void loop(){
  if(t_heartbeat <= 0){
    t_heartbeat = KEEP_ALIVE_MAX;
    send_mesg(HEARTBEAT,ALIVE);
  }
  dec_timers();
  receive_mesg();
  long distance = getDistance(); // Use function to calculate the distance
  // If you are outside of range
  if (distance > ULTRASONIC_HIGH){
    // If a message hasn't been sent yet
    if (!tripped && trip_count >= TRIP_MAX) {
      send_mesg(ULTRASONIC_TRIP, ULTRASONIC_TRIP);
      tripped = true;
      trip_count = 0;
    }
    trip_count += 1;
  // Inside of valid range
  } else {
    tripped = false;
    //trip_count = 0;
  }
}


long getDistance() {
  digitalWrite(TriggerPin, LOW);
  delayMicroseconds(2);
  digitalWrite(TriggerPin, HIGH);
  delayMicroseconds(10); // 10us high
  digitalWrite(TriggerPin, LOW);
  // Waits for the echo pin to get high
  long time = pulseIn(EchoPin,HIGH);

  // Calculates the Distance in mm
  // ((time)*(Speed of sound))/ toward and backward of object) * 10

  return ((time /2.9) / 2); // Actual calculation in mm
  return time / 74 / 2; // Actual calculation in inches
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
      default:
        send_mesg(RECEIVE, mesg_code);
        break;
    }
    // After handling data, reset the message code
    mesg_code = NO_MESSAGE;// Reset message code
    data = NO_MESSAGE;
  }
}


// Decrements all delay timers
void dec_timers(){
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

