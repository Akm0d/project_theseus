// Laser board test sketch

// 6 laser diodes
#define L0_PIN 2 // D2
#define L1_PIN 3 // D3
#define L2_PIN 4 // D4
#define L3_PIN 5 // D5
#define L4_PIN 6 // D6
#define L5_PIN 7 // D7

// 6 photoresistors
#define PRES0_PIN 14 // A0
#define PRES1_PIN 15 // A1
#define PRES2_PIN 16 // A2
#define PRES3_PIN 17 // A3
#define PRES4_PIN 18 // A4
#define PRES5_PIN 19 // A5

// LED strip (Christmas lights)
#define LEDSTRIP_PIN 9 // D9

// Other constants
#define BAUD_RATE 115200

// Helpful macros
#define PIN_HIGH(pin) digitalWrite(pin,HIGH)
#define PIN_LOW(pin) digitalWrite(pin,LOW)
#define PIN_TOGGLE(pin) digitalWrite(pin,!digitalRead(pin))

// Function prototypes
void testLasers();
void testPhotoresistors();
void testLedStrip();
void testAll();

void setup() {
  pinMode(L0_PIN, OUTPUT);
  pinMode(L1_PIN, OUTPUT);
  pinMode(L2_PIN, OUTPUT);
  pinMode(L3_PIN, OUTPUT);
  pinMode(L4_PIN, OUTPUT);
  pinMode(L5_PIN, OUTPUT);

  Serial.begin(BAUD_RATE);
  delay(2000);
  Serial.println("Start testing.");
  testLasers();
  PIN_HIGH(LEDSTRIP_PIN);

  // Turn on all laser diodes
  for (int i = 0; i < 6; i++) {
    PIN_HIGH(L0_PIN+i);
  }
//  PIN_HIGH(L0_PIN);
  Serial.println("Start looping.");
}

void loop() {
  testPhotoresistors();
  delay(1000);
}

void testLasers() {
  int i;
  
  // Turn them on one at a time
  PIN_HIGH(L0_PIN);
  for (i = 0; i < 5; i++) {
    delay(1000);
    PIN_LOW(L0_PIN+i); // turn off current pin
    PIN_HIGH(L0_PIN+i+1);
  }
  PIN_LOW(L0_PIN+i);
  PIN_HIGH(L5_PIN);
  delay(1000);
  PIN_LOW(L5_PIN);
  delay(1000);
  
  // Turn them all on and off
  for (int j = 0; j < 2; j++) {
    for (i = 0; i < 6; i++) {
      PIN_TOGGLE(L0_PIN+i);
    }
    delay(1000);
  }
}

void testPhotoresistors() {
  // Read photoresistors
  Serial.println("Photoresistors:");
  for (int i = 0; i < 6; i++) {
    int val = analogRead(PRES0_PIN+i);
    Serial.println(val);
  }
}

void testLedStrip() {
  PIN_HIGH(LEDSTRIP_PIN);
  delay(5000);
  PIN_LOW(LEDSTRIP_PIN);
}

