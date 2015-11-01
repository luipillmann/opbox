#!/usr/bin/python
import serial
import syslog
import time

#The following line is for serial over GPIO
port = '/dev/tty.usbmodem1411' # note I'm using Mac OS-X

ard = serial.Serial(port,9600,timeout=5)
time.sleep(2) # wait for Arduino


def readSerial():
	# Serial read section
    msg = ard.read(ard.inWaiting()) # read all characters in buffer
    print ("Message from arduino: ")
    print (msg)
    return

def writeSerial(txt):
	# Serial write section
    ardCmd = txt;
    ard.flush()
    print ("Python value sent: ")
    print (txt)
    ard.write(txt)
    time.sleep(1) # I shortened this to match the new value in your Arduino code
    return

readSerial()
user_txt = raw_input('Type command: ');
writeSerial(user_txt)

while (True):
	readSerial()
	time.sleep(1)
else:
    print "Exiting"
exit()

