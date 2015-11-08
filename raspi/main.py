#!/usr/bin/python

import defines
from serial_ard import SerialArduino 
from file_handler import FileHandler
from chart import Chart

#The following line is for serial over GPIO
port = '/dev/tty.usbmodem1411' # note I'm using Mac OS-X
baud_rate = 9600
#port = '/dev/ttyACM0' # Raspberry Pi's port

user_file = ''
start_time = ''

#### Code itself ####

# Objects
ard = SerialArduino(port, baud_rate)
txt = FileHandler(user_file)

user_file = raw_input('Type TXT file name: ')
txt.set_name(user_file)

user_cmd = raw_input('Type command: ');
ard.write(user_cmd)

# Main reading loop
print 'Reading serial...'

i = 0
while (i < 10 + 2):
	msg = ard.read()
	if (msg[0] == defines.LOG_HEADER) or (msg[0] == defines.STARTTIME_HEADER) or (msg[0] == defines.MEASUREMENT_HEADER):
		txt.write(msg)
	#writeToFile()
	#time.sleep(1)
	else:
		print 'File content not readable at iteration: ' + str(i)

	i = i + 1
	

txt.read()
ard.write('C0')
print "Exiting"



data = txt.parse()
chart1 = Chart(txt.get_name(), 'default', data)
chart1.plot()
#plotChart(data[0], data[1], txt.get_name())

exit()
