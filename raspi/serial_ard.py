"""

High level serial class for this specific application

Serial communication code based on Peter Gibson's (http://stackoverflow.com/questions/24074914/python-to-arduino-serial-read-write)

"""

import serial
import time
import defines

class SerialArduino(object):
    """A class that makes the serial operations."""
    def __init__(self, port, baud):
       	self.port = port
       	self.baud = baud
    	self.ard = serial.Serial(self.port,self.baud,timeout=5)
		#time.sleep(2) # wait for Arduino

    def read(self):
    	# Serial read section
        #msg = ard.read(ard.inWaiting()) # read all characters in buffer
        msg = self.ard.readline()
        #print msg;
        #print ("Message from arduino: ")
        return msg

    def write(self, txt):
    	# Serial write section
        ardCmd = txt;
        self.ard.flush()
        print ('Python value sent: ')
        print (txt)
        self.ard.write(txt)
        time.sleep(1) # I shortened this to match the new value in your Arduino code
        return