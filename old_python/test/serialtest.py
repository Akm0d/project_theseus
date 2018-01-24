import serial
import array
from time import sleep


'''
  Message format: XY Z   ex. 01 12355
  X - ID number of arduino sending the message
  Y - ID number for contents of the package ex. pot value
  Z - data

  For packets sent to the arduino the X val in the message format is arbitrary.
  The RPi knows what arduino it is sending the message to.

  From arduino:
    - 10    # switches value
    - 11    # potentiometer value
    - 12    # red wire value
    - 13    # blue wire value
    - 14    # arduino ID number report
    - 15    # solenoid value

  To arduino:
    - 11    # LED data
    - 12    # solenoid position
    - 13    # send arduino ID number
'''

#TODO: make a command that has the arduino report it's ID number

ser = serial.Serial('/dev/ttyUSB0', 115200)
# supossedly when python connects to the arduino it sends it a reset signal.
# If you don't give the arduino time to reset, then things break.
sleep(1)

#bit values of the switches
sw0 = 0x1
sw1 = 0x2
sw2 = 0x4
sw3 = 0x8
sw4 = 0x10

#init values
pot = 0
switches = 0x0
rwire = 0x0
bwire = 0x0

#set to True to test sending the packet to the arduino
DEBUG = False

while DEBUG == False:
    #wait for a packet
    if ser.inWaiting():
        temp = ser.readline()

        #parse the packet
        temp = temp.decode("utf-8")
        temp =  temp.split(' ')

        if len(temp) == 2:
            code = temp[0]
            data = temp[1][:-2]

            if code == "10":
                switches = int(data)
            elif code == "11":
                pot =  int(data)
            elif code == "12":
                rwire = int(data)
                # print("red wire val: %d" % rwire)
            elif code == "13":
                bwire = int(data)
                # print("blue wire val: %d" % bwire)
            elif code == "14":
                print("arduino code: %d" % int(data))

            #Logic for choosing what leds are on
            #TODO: Turn this into a function and call it everytime a '00' or '01'
            #packet arrives
            leds = 0x0
            if((switches & sw0) and (pot < 500)):
                leds = 0x30
            elif((switches & sw1) and (pot < 500)):
                leds = 0x0C
            elif((switches & sw2) and (pot < 500)):
                leds = 0xC0
            elif((switches & sw3) and (pot < 500)):
                leds = 0x03

            #writes command to arduino, in this case, 01 <led val>
            #TODO: this should also be a function
            ser.write(array.array('B', [0x11, leds]).tostring())


# this is test code for sending packets to the arduino
while DEBUG == True:
    ser.write(array.array('B', [0x01, 0xC0]).tostring())
    sleep(1)
    tf = True
    while tf:
        while ser.inWaiting():
            temp = ser.readline()
            print(temp)
            # import pdb; pdb.set_trace()
        tf = False
                # sleep(.5)
