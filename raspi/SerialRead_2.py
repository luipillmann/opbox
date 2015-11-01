#!/usr/bin/python
import serial
import syslog
import time
import plotly.plotly as py
import plotly.graph_objs as go

LOG_HEADER = 'L'         # Header tag for logging messages
STARTTIME_HEADER = 'S'   # Header tag for start time message
MEASUREMENT_HEADER = 'M' # Header tag for serial measurement message
CMD_HEADER = 'C'         # Header tag for serial command message
TIME_HEADER = 'T'        # Header tag for serial time sync message

#The following line is for serial over GPIO
port = '/dev/tty.usbmodem1411' # note I'm using Mac OS-X

ard = serial.Serial(port,9600,timeout=5)
time.sleep(2) # wait for Arduino

test_file = "test.txt"


def printSerial():
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
    print ("Python value sent: ")
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
	with open(textfile) as f:
		content = f.readlines()
		for line in content:
			if line[0] == STARTTIME_HEADER:
				start_time = line[1:]
			elif line[0] == MEASUREMENT_HEADER:
				line_measures.append(line[1:])

	print "\n\nStart time: " + start_time;
	print "\n\nData extracted"
	print line_measures

	pairs = []

	for line in line_measures:
		[pairs.append(x.strip()) for x in line.split(';')]
	
	print "\n\nPairs of data"
	print pairs

	m_times = []
	m_values = []

	for item in pairs:
		aux = item.partition(',');
		m_times.append(aux[0])
		m_values.append(aux[2])

		#[m_times.append(x.strip()) for x in item.partition(',')[]]
		#[m_values.append(x.strip()) for x in item.rsplit(',',1)]

	print "\n\nTime and values"
	print m_times
	print m_values
	print len(m_values) == len(m_times)
	plotChart(m_times, m_values)

def plotChart(x_values, y_values):
	trace0 = go.Scatter(
	    x=x_values,
	    y=y_values,
	    mode='markers'
	)
	data = [trace0]
	plot_url = py.plot(data, filename='LDR-reader')


# Code itself
printSerial()
user_txt = raw_input('Type command: ');
writeSerial(user_txt)

i = 0

while (i < 1000):
	msg = printSerial()
	if (msg[0] == LOG_HEADER) or (msg[0] == STARTTIME_HEADER) or (msg[0] == MEASUREMENT_HEADER):
		writeFile(test_file, msg)
	#writeToFile()
	#time.sleep(1)
	i = i + 1
else:
	readFile(test_file)
	print "Exiting"

parseFile(test_file)

exit()

