#!/usr/bin/python
# Serial communication code on Peter Gibson's (http://stackoverflow.com/questions/24074914/python-to-arduino-serial-read-write)

import serial
import syslog
import time
import plotly.plotly as py
import plotly.graph_objs as go
import os

LOG_HEADER 			= 'L' # Header tag for logging messages
STARTTIME_HEADER 	= 'S' # Header tag for start time message
MEASUREMENT_HEADER 	= 'M' # Header tag for serial measurement message
CMD_HEADER 			= 'C' # Header tag for serial command message
TIME_HEADER 		= 'T' # Header tag for serial time sync message

#The following line is for serial over GPIO
port = '/dev/tty.usbmodem1411' # note I'm using Mac OS-X
#port = '/dev/ttyACM0' # Raspberry Pi's port


ard = serial.Serial(port,9600,timeout=5)
time.sleep(2) # wait for Arduino

test_file = 'test.txt'
user_file = ''
start_time = ''

def readSerial():
	# Serial read section
    #msg = ard.read(ard.inWaiting()) # read all characters in buffer
    msg = ard.readline()
    #print msg;
    #print ("Message from arduino: ")
    return msg

def writeSerial(txt):
	# Serial write section
    ardCmd = txt;
    ard.flush()
    print ('Python value sent: ')
    print (txt)
    ard.write(txt)
    time.sleep(1) # I shortened this to match the new value in your Arduino code
    return

def writeFile(textfile, txt):
	with open(textfile, "a") as f:
		f.write(txt) # python will convert \n to os.linesep

def readFile(textfile):
	with open(textfile) as f:
		content = f.readlines()
		print content

def parseFile(textfile):
	line_measures = []
	line_logs = []
	with open(textfile) as f:
		content = f.readlines()
		for line in content:	# iterates through lines and checks header
			if line[0] == LOG_HEADER:
				line_logs.append(line[1:])
			elif line[0] == STARTTIME_HEADER:
				start_time = line[1:]
				start_time = start_time[:4] #
				print '\n\nStart time: '
				print start_time
				globals()['start_time'] = start_time # sets global variable
			elif line[0] == MEASUREMENT_HEADER:
				line_measures.append(line[1:])

	pairs = []

	for line in line_measures:
		[pairs.append(x.strip()) for x in line.split(';')]

	m_times = []
	m_values = []

	for item in pairs:
		aux = item.partition(',');
		m_times.append(aux[0])
		m_values.append(aux[2])

	print '\n\nTime and values'
	print m_times
	print m_values
	textfile = os.path.splitext(textfile)[0] # removes filename extension (.txt)
	plotChart(m_times, m_values, textfile)


def plotChart(x_values, y_values, plot_name):

	print '\n\n\nEntering PLOT'
	print start_time
	print repr(start_time)
	print '\n\n\nConversion next'
	start_t = float(start_time)
	x_values = [(float(x)-start_t)/1000 for x in x_values] # converts values to float and for X, removes offset and divides by 1000 (data in ms)
	y_values = [float(y) for y in y_values]

	trace0 = go.Scatter(
	    x=x_values,
	    y=y_values,
	    mode='markers'
	)
	data = [trace0]
	if plot_name == '':
		plot_name = 'default_plot'
	plot_url = py.plot(data, filename=plot_name)

def initInterface():
	for i in xrange(1,80):
		print "-"
	print "---------------  OPBOX CLI INTERFACE -------------------"



#### Code itself ####
readSerial()
user_file = raw_input('Type TXT file name: ')
user_file = user_file + '.txt'
user_txt = raw_input('Type command: ');
writeSerial(user_txt)

i = 0

while (i < 100):
	msg = readSerial()
	if (msg[0] == LOG_HEADER) or (msg[0] == STARTTIME_HEADER) or (msg[0] == MEASUREMENT_HEADER):
		writeFile(user_file, msg)
	#writeToFile()
	#time.sleep(1)
	i = i + 1
else:
	readFile(user_file)
	print "Exiting"

parseFile(user_file)

exit()
