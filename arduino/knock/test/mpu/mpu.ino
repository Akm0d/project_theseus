#include <Servo.h>

Servo pan; 
Servo tilt; 

void setup(){
	pan.attach(3); 
	tilt.attach(5); 
}

int pos = 0; 

void loop(){
	pan.write(pos); 
	tilt.write(180-pos); 

	if(pos == 180){
		pos = 0; 
	}
	else{
		pos += 20; 
	}

	delay(1500); 
}