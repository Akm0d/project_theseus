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
#define POT_PIN 16 // A2
#define SW0_PIN 12 // D12
#define SW1_PIN 11 // D11
#define SW2_PIN 10 // D10
#define SW3_PIN 14 // A0
#define SW4_PIN 15 // A1
#define FAN_PIN 13 // D13
#define SOLENOID_PIN 17 // A3

#define BAUD_RATE 115200

#define PIN_HIGH(pin) digitalWrite(pin, HIGH)
#define PIN_LOW(pin) digitalWrite(pin, LOW)
#define PIN_TOGGLE(pin) digitalWrite(pin, !digitalRead(pin))

void testLeds();
void testRedBlueWire();
void testSwitchesAndPot();
void testSolenoid();

void setup() {
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
  Serial.begin(BAUD_RATE);

  testLeds();
  PIN_HIGH(FAN_PIN);
  PIN_HIGH(SOLENOID_PIN);
  Serial.println("Start testing:");
}

void loop() {
  // Do the following 10 times per second.
  testRedBlueWire();
  testSwitchesAndPot();

  // Do the following only once per second.
  static int i = 0;
  static int j = 0;
  i++;
  j++;
  if (i >= 10) {
    PIN_TOGGLE(LED5_PIN);
    PIN_TOGGLE(LED6_PIN);
    PIN_TOGGLE(LED7_PIN);
    i = 0;
  }
  // Do the following once every five seconds.
  if (j >= 50) {
    PIN_TOGGLE(FAN_PIN);
    PIN_TOGGLE(SOLENOID_PIN);
    j = 0;
  }
  
  delay(100);
}

// Turn each LED on one at a time.
// Then all on and off at the end.
void testLeds() {
  PIN_HIGH(LED0_PIN);
  delay(1000);
  PIN_LOW(LED0_PIN);
  PIN_HIGH(LED1_PIN);
  delay(1000);
  PIN_LOW(LED1_PIN);
  PIN_HIGH(LED2_PIN);
  delay(1000);
  PIN_LOW(LED2_PIN);
  PIN_HIGH(LED3_PIN);
  delay(1000);
  PIN_LOW(LED3_PIN);
  PIN_HIGH(LED4_PIN);
  delay(1000);
  PIN_LOW(LED4_PIN);
  PIN_HIGH(LED5_PIN);
  delay(1000);
  PIN_LOW(LED5_PIN);
  PIN_HIGH(LED6_PIN);
  delay(1000);
  PIN_LOW(LED6_PIN);
  PIN_HIGH(LED7_PIN);
  delay(1000);
  PIN_LOW(LED7_PIN);
  delay(1000);

  int i;
  for (i = 0; i < 2; i++) {
    PIN_TOGGLE(LED0_PIN);
    PIN_TOGGLE(LED1_PIN);
    PIN_TOGGLE(LED2_PIN);
    PIN_TOGGLE(LED3_PIN);
    PIN_TOGGLE(LED4_PIN);
    PIN_TOGGLE(LED5_PIN);
    PIN_TOGGLE(LED6_PIN);
    PIN_TOGGLE(LED7_PIN);
    delay(1000);
  }
}

// If the pin reads HIGH, then the wire is still attached.
// If the pin reads LOW, then the wire has been detached.
void testRedBlueWire() {

  // Test red wire
  static int redWireState = HIGH;
  int redWire = digitalRead(RED_WIRE_PIN);
  switch(redWireState) {
    case HIGH:
      if (!redWire) {
        redWireState = LOW;
        Serial.println("Red Wire detached");
      }
      break;
    case LOW:
      if (redWire) {
        redWireState = HIGH;
        Serial.println("Red Wire reattached");
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
        Serial.println("Blue Wire detached");
      }
      break;
    case LOW:
      if (blueWire) {
        blueWireState = HIGH;
        Serial.println("Blue Wire reattached");
      }
      break;
    default:
      blueWireState = HIGH;
      break;
  }
}

void testSwitchesAndPot() {
  
  // Read switches
  boolean sw0 = digitalRead(SW0_PIN);
  boolean sw1 = digitalRead(SW1_PIN);
  boolean sw2 = digitalRead(SW2_PIN);
  boolean sw3 = digitalRead(SW3_PIN);
  boolean sw4 = digitalRead(SW4_PIN);

  // Set LED to corresponding switch state
  digitalWrite(LED0_PIN, sw0);
  digitalWrite(LED1_PIN, sw1);
  digitalWrite(LED2_PIN, sw2);
  digitalWrite(LED3_PIN, sw3);
  digitalWrite(LED4_PIN, sw4);

  Serial.print("Switches: ");
  Serial.print(sw0);
  Serial.print(sw1);
  Serial.print(sw2);
  Serial.print(sw3);
  Serial.print(sw4);
  Serial.println("");
  
  // Read pot
  int pot = analogRead(POT_PIN);
  
  // Print pot value
  Serial.print("Pot value: ");
  Serial.println(pot);
}

