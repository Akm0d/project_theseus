/*
*  ciruit diagram found here: http://bildr.org/2012/03/rfp30n06le-arduino/
*  The arduino nano does not output enough current to work the gate on a power mosfet. 
*  We will need to find an alternate solution to how to work this.
*/

const int onOff = 3;
const int LED = 13; 

void setup(){
  pinMode(onOff, OUTPUT); 
  pinMode(LED, OUTPUT);
  Serial.begin(9600); 
  Serial.println("Initialized"); 
}

void loop(){
  digitalWrite(LED, HIGH);
    digitalWrite(onOff, HIGH); 
  delay(1000); 
    digitalWrite(LED, LOW);
    digitalWrite(onOff, LOW); 
    delay(1000); 
}
