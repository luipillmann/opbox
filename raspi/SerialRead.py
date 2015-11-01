import serial
import syslog
import time

ser = serial.Serial('/dev/cu.usbmodem1411') # MacBook's
#ser = serial.Serial('/dev/ttyACM0') # RPi's

print 'Reading from serial\n'

while True:
    txt = raw_input()
    print txt.upper()
    pkg = ser.readline()
    pass


    #pkg = ser.readline()
    #print pkg
    #[x.strip() for x in pkg.split(',')]
    #for p in x: print p
