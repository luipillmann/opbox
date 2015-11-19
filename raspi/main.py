#!/usr/bin/python
import os
import time
import defines
from serial_ard import SerialArduino 
from file_handler import FileHandler
from chart import Chart
from table import Table
from interface import ConsoleInterface


#The following line is for serial over GPIO
#port = '/dev/tty.usbmodem1411' # note I'm using Mac OS-X
baud_rate = 9600
port = '/dev/ttyACM0' # Raspberry Pi's port

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

def parse_line(line):
	values = []
	[values.append(x.strip()) for x in line.split(',')]
	
	m_time = ''
	m_temp = ''
	m_fbar = ''
	m_lint = ''

	for item in values:
		if item[0] == defines.MEASUREMENT_HEADER:
			m_time = item[1:]
		elif item[0] == defines.TEMPERATURE_HEADER:
			m_temp = item[1:]
		elif item[0] == defines.FORCE_BAR_HEADER:
			m_fbar = item[1:]
		elif item[0] == defines.LIGHT_HEADER:
			m_lint = item[1:]

	# Processes values to float. Time to seconds
	start_t = txt.get_start_time()
	m_time = int((int(m_time)-start_t)/1000)
	#temp_values = [float(y) for y in m_temp]
	#fbar_values = [float(y) for y in m_fbar]
	#lint_values = [float(y) for y in m_lint]
	
	row = [str(m_time), m_temp, m_fbar, m_lint] #data are float values

	return row	


#### Code itself ####

# Objects declaration
ard = SerialArduino(port, baud_rate)
txt = FileHandler(user_file)
dat = Table('data') 
cli = ConsoleInterface(dat) # binds data table to interface object

cli.init_interface() # prints header
op = cli.start_menu()

if op.upper() == 'Y':
	#cli.setup_interface()
	user_file = raw_input('Type TXT file name: ')
	txt.set_name(user_file)

	cli.show_warning('Hit Ctrl-C to stop acquisition')
	cli.getch()

	### !!! BIG INCONSISTENCY RIGHT HERE !!!

	ard.write('C0') # stops Arduino just in case 
	ard.write('C1') # C1 is the command to start C = cmd, 1 sets Arduino 'flag' to 1
	msg = ard.read()
	txt.write(msg) # saves first data to txt file!
	if 'started' in msg:
		print '<<<Acquisition has started.'

	### GOTTA FIX THIS HAND SHAKE STEP LATER
	
	#dat.add_rows(build_rows(dtime, dtemp, dfbar, dilux))
	#cli.draw_table()

	# Main reading loop, stops when user hits Ctrl-C. After that, finishing tasks and infos are done and printed
	try: 
	    i = 0
	    while True:
	    	msg = ard.read_line()
	    	if (msg[0] == defines.LOG_HEADER) or (msg[0] == defines.STARTTIME_HEADER) or (msg[0] == defines.MEASUREMENT_HEADER):
	    		txt.write(msg)
	    		#print 'Wrote to file reading ' + str(i)

	    		# parses line and adds to data table
	    		row = ['','','','','','','','']
	    		if msg[0] == defines.MEASUREMENT_HEADER:
	    			row = dat.add_row(parse_line(msg))
	    			#print 'row added: '
	    			#print parse_line(msg)
	    		#cli.update_interface()
	    		if i==0:
	    			cli.init_interface()
	    			cli.draw_table_header()
	    		cli.cprint_row([row[0],'',row[1],'',row[2],'',row[3],''])            

	    	else:
	    		print 'File content not readable at iteration: ' + str(i)	
	    	i = i + 1
	except KeyboardInterrupt:
	    print '\n'
	    cli.print_centered_with_symbol('','-')
	    print 'Acquisition has stopped.'
	    print '\n\n'

	if cli.plot_menu().upper() == 'Y':
		# processes data and plots chart in plotly
		data = txt.parse()
		chart1 = Chart(txt.get_name(), 'default', data)
		chart1.plot_mult()
else:
	pass

ard.write('C0') # sends command to Arduino stop acquisition 
print '\nExiting...\n'

if op.upper() == 'Y':
	path = os.path.dirname(os.path.abspath(__file__))
	print 'Acquired data saved in ' + path + '/' + txt.get_name() + '.txt'
	print '\n'
	

#plotChart(data[0], data[1], txt.get_name())

exit()
