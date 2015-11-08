import syslog
import os

class FileHandler(object):
	"""A class that takes care of files in .txt format."""
    def __init__(self, textfile):
       	self.textfile = textfile + '.txt' #adds extension

    def file_name(self):
    	return self.textfile

    def write(self, txt):
    	with open(self.textfile, "a") as f:
    		f.write(txt) # python will convert \n to os.linesep

    def read(self):
    	with open(self.textfile) as f:
    		content = f.readlines()
    		print content

    def parse(self):
    	line_measures = []
    	line_logs = []
    	with open(self.textfile) as f:
    		content = f.readlines()
    		for line in content:	# iterates through lines and checks header
    			if line[0] == defines.LOG_HEADER:
    				line_logs.append(line[1:])
    			elif line[0] == defines.STARTTIME_HEADER:
    				start_time = line[1:]
    				start_time = start_time[:4] #
    				#print '\n\nStart time: '
    				#print start_time
    				globals()['start_time'] = start_time # sets global variable
    			elif line[0] == defines.MEASUREMENT_HEADER:
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

    	#print '\n\nTime and values'
    	#print m_times
    	#print m_values
