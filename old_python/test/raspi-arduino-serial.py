from time import sleep
import serial

ser1 = serial.Serial('/dev/ttyUSB0', 9600)
ser2 = serial.Serial('/dev/ttyUSB1', 9600)
ser3 = serial.Serial('/dev/ttyUSB2', 9600)
ser4 = serial.Serial('/dev/ttyUSB3', 9600)

while True: 
    sleep(.8)
    if ser1.inWaiting():
        print(ser1.readline())
    if ser2.inWaiting(): 
        print(ser2.readline())
    if ser3.inWaiting():
        print(ser3.readline())
    if ser4.inWaiting(): 
        print(ser4.readline())
