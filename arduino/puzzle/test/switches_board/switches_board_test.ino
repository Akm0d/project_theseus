// Test sketch for switches/pot board.

#define LED_PIN 2 // D2
#define POT_PIN 16 // A2
#define SW0_PIN 12 // D12
#define SW1_PIN 11 // D11
#define SW2_PIN 10 // D10
#define SW3_PIN 14 // A0
#define SW4_PIN 15 // A1
#define BAUD_RATE 115200

void setup() {
  Serial.begin(BAUD_RATE);
  pinMode(LED_PIN, OUTPUT);
  pinMode(SW0_PIN, INPUT);
  pinMode(SW1_PIN, INPUT);
  pinMode(SW2_PIN, INPUT);
  pinMode(SW3_PIN, INPUT);
  pinMode(SW4_PIN, INPUT);
}

void loop() {
  // Read switches
  int sw0 = digitalRead(SW0_PIN);
  int sw1 = digitalRead(SW1_PIN);
  int sw2 = digitalRead(SW2_PIN);
  int sw3 = digitalRead(SW3_PIN);
  int sw4 = digitalRead(SW4_PIN);

  // Turn on LED if any switch is on
  digitalWrite(LED_PIN, sw0 || sw1 || sw2 || sw3 || sw4);
  
  // Read pot
  int pot = analogRead(POT_PIN);

  // Print pot value
  Serial.println(pot);
  delay(100);
}

