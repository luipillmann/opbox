#!/usr/bin/python
import time
import defines
from serial_ard import SerialArduino 
from file_handler import FileHandler
from chart import Chart
from table import Table
from interface import ConsoleInterface


#The following line is for serial over GPIO
port = '/dev/tty.usbmodem1411' # note I'm using Mac OS-X
baud_rate = 9600
#port = '/dev/ttyACM0' # Raspberry Pi's port

user_file = ''
start_time = ''
dtime = ['19:00:32', '19:00:32', '19:00:33', '19:00:34']
dtemp = ['23.0', '23.0', '23.0', '23.0']
dfbar = ['0.0', '12.0', '87.2', '0.0']
dilux = ['60.1', '69.1', '62.1', '62.1']

def build_rows(ptime, ptemp, pfbar, pilux):
	rows = []
	if len(ptime) == len(ptemp) == len(pfbar) == len(pilux):
		for x, val in enumerate(ptime):
			rows.append([ptime[x], ptemp[x], pfbar[x], pilux[x]])
	else:
		print 'ERROR: Data values not the same lenght.'

	return rows

def getch():
	import sys, tty, termios
	old_settings = termios.tcgetattr(0)
	new_settings = old_settings[:]
	new_settings[3] &= ~termios.ICANON
	try:
		termios.tcsetattr(0, termios.TCSANOW, new_settings)
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(0, termios.TCSANOW, old_settings)
	return ch


#### Code itself ####

# Objects declaration
ard = SerialArduino(port, baud_rate)
txt = FileHandler(user_file)
dat = Table('data') 
cli = ConsoleInterface(dat) # binds data table to interface object

cli.init_interface() # prints header
op = cli.show_menu()

if op.upper() == 'Y':
	#cli.setup_interface()
	user_file = raw_input('Type TXT file name: ')
	txt.set_name(user_file)

	
	ard.write('C1')
	time.sleep(3)
	ard.flush()
	msg = ard.read()
	print msg
	if 'a' in msg:
		print 'Aquisition has started.'

	txt.write(msg)

	dat.add_rows(build_rows(dtime, dtemp, dfbar, dilux))
	cli.draw_table()

	# Main reading loop
	print 'Reading serial...'

	i = 0
	while (i < 10 + 2):
		msg = ard.read_line()
		if (msg[0] == defines.LOG_HEADER) or (msg[0] == defines.STARTTIME_HEADER) or (msg[0] == defines.MEASUREMENT_HEADER):
			txt.write(msg)
			print 'Wrote to file reading ' + str(i)
		#writeToFile()
		#time.sleep(1)
		else:
			print 'File content not readable at iteration: ' + str(i)

		i = i + 1

	data = txt.parse()
	chart1 = Chart(txt.get_name(), 'default', data)
	chart1.plot()
else:
	pass

ard.write('C0')
print "Exiting"




#plotChart(data[0], data[1], txt.get_name())

exit()
