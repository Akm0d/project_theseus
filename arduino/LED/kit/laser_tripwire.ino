/** Laser Tripwire */
/** Created by Tyler Johnson */
// 6 laser diodes
#define L0_PIN 3 // D2
#define L1_PIN 2 // D3
#define L2_PIN 4 // D4
#define L3_PIN 5 // D5
#define L4_PIN 6 // D6
#define L5_PIN 7 // D7

// 6 photoresistors A0-5 or D14-19
#define PRES0_PIN 18
#define PRES1_PIN 19
#define PRES2_PIN 14
#define PRES3_PIN 15
#define PRES4_PIN 16
#define PRES5_PIN 17

// LED strip (Christmas lights)
#define LEDSTRIP_PIN 9 // D9

// Serial
#define SECOND 50000 // This value may change as the code gets larger, it determines the delay for one second
#define BAUD_RATE 115200
#define ARDUINO_NUMBER '4'
#define RECEIVE 'c'
#define SUCCESS 's'
#define FAILURE 'f'
#define HEARTBEAT 'h'
#define ALIVE 'a'
#define TRIPPED 'T'
//incoming
#define RANDOMIZE_LASERS 'R'
#define LED_STRIP_ON 'N'
#define LED_STRIP_OFF 'F'
#define RESET 'r'
#define NO_MESSAGE -1
// Timing
#define RECEIVE_MAX SECOND / 200
// The rate for sending heartbeats
// It has to be frequent, but no so often that it drowns out other signals
#define KEEP_ALIVE_MAX SECOND * 2
#define FLASH_MAX SECOND / 5

// The resistance must be greater than this value for the LED to be considered ON
#define LIGHTS_OFF 300
/********************************************/
// Delay timers
static unsigned int t_receive = 0;
static long unsigned int t_second = 0;
static long unsigned int t_heartbeat = 0;
static unsigned int t_flash = 0;

// Laser pattern
int laser_pattern = 0x00;
bool flash_enable = false;

// Serial
char data = NO_MESSAGE;
char mesg_code = NO_MESSAGE;

/***********Function Prototypes**************/
//Arduino
void dec_timers();
void randomize_lasers();
void detect_trip();
void flash_lights(bool);
void show_pattern(int);

//Serial
void receive_mesg();
void send_mesg(char code, char data);

/********************************************/

void setup(){
  pinMode(L0_PIN, OUTPUT);
  pinMode(L1_PIN, OUTPUT);
  pinMode(L2_PIN, OUTPUT);
  pinMode(L3_PIN, OUTPUT);
  pinMode(L4_PIN, OUTPUT);
  pinMode(L5_PIN, OUTPUT);
  pinMode(LEDSTRIP_PIN, OUTPUT);
  Serial.begin(BAUD_RATE);
  randomSeed(analogRead(PRES0_PIN) ^ analogRead(PRES5_PIN));
  randomize_lasers();
}

void loop(){
  if(!t_heartbeat){
    t_heartbeat = KEEP_ALIVE_MAX;
    send_mesg(HEARTBEAT,ALIVE);
  }
  dec_timers();
  receive_mesg();
  detect_trip();
  if (flash_enable && !t_flash){
    show_pattern(random(0, 0x3f));
    t_flash = FLASH_MAX;
  }
}


bool pr_values[6];
/*
* Sample the photoresistors corresponding to each active laser
* If the value of one of these phooresistors is less than LIGHTS_OFF then send the tripped signal to rpi
*/
void detect_trip(){
    // If the PHOTO_DIODE's resistance drops below the calibrated value
    if (!flash_enable) {
      if(laser_pattern & 1){
         bool new_value = analogRead(PRES0_PIN) < LIGHTS_OFF;
         if (new_value && !pr_values[0]){
           send_mesg(TRIPPED, '0');
         }
         pr_values[0] = new_value;
      }
      if(laser_pattern & 2){
         bool new_value = analogRead(PRES1_PIN) < LIGHTS_OFF;
         if (new_value && !pr_values[1]){
           send_mesg(TRIPPED, '1');
         }
         pr_values[1] = new_value;
      }
      if(laser_pattern & 4){
         bool new_value = analogRead(PRES2_PIN) < LIGHTS_OFF;
         if (new_value && !pr_values[2]){
           send_mesg(TRIPPED, '2');
         }
         pr_values[2] = new_value;
      }
      if(laser_pattern & 8){
         bool new_value = analogRead(PRES3_PIN) < LIGHTS_OFF;
         if (new_value && !pr_values[3]){
           send_mesg(TRIPPED, '3');
         }
         pr_values[3] = new_value;
      }
      if(laser_pattern & 16){
         bool new_value = analogRead(PRES4_PIN) < LIGHTS_OFF;
         if (new_value && !pr_values[4]){
           send_mesg(TRIPPED, '4');
         }
         pr_values[4] = new_value;
      }
      if(laser_pattern & 32){
         bool new_value = analogRead(PRES5_PIN) < LIGHTS_OFF;
         if (new_value && !pr_values[5]){
           send_mesg(TRIPPED, '5');
         }
         pr_values[5] = new_value;
      }     
    }
}

const int laser_configurations[] = {
  5, 10, 20, 40, 
  9, 18, 36, 
  17, 34,
  33
};
const int num_configurations = sizeof(laser_configurations)/sizeof(int);

// Choose a random configuration from a list
// Lasers full would be laser_pattern = 0x3f
// Only two lasers active at a time
// No adjacent lasers are active
void randomize_lasers(){
  laser_pattern = laser_configurations[random(0, num_configurations)];
  show_pattern(laser_pattern);
}

void show_pattern(int pattern){
  // Light up the lasers found in the pattern
  digitalWrite(L0_PIN, (pattern & 1)? HIGH: LOW);
  digitalWrite(L1_PIN, (pattern & 2)? HIGH: LOW);
  digitalWrite(L2_PIN, (pattern & 4)? HIGH: LOW);
  digitalWrite(L3_PIN, (pattern & 8)? HIGH: LOW);
  digitalWrite(L4_PIN, (pattern & 16)? HIGH: LOW);
  digitalWrite(L5_PIN, (pattern & 32)? HIGH: LOW);
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
      case RANDOMIZE_LASERS:
        randomize_lasers();
        break;
      case LED_STRIP_ON:
        flash_enable = true;
        break;
      case LED_STRIP_OFF:
        flash_enable = false;
        show_pattern(laser_pattern);
        break;
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
  if (t_second) t_second--;
  if (t_receive) t_receive--;
  if (t_heartbeat) t_heartbeat--;
  if (t_flash) t_flash--;
}

void send_mesg(char code,char data){
  Serial.print(ARDUINO_NUMBER);
  Serial.print(" ");
  Serial.print(code);
  Serial.print(" ");
  Serial.println(data);
}
