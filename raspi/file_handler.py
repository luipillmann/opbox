import syslog
import os
import defines

class FileHandler(object):
	"""A class that takes care of files in .txt format."""
	def __init__(self, textfile):
		self.name = textfile
		self.textfile = textfile + '.txt' #adds extension

	def set_name(self, textfile):
		self.name = textfile
		self.textfile = textfile + '.txt'

	def get_name(self):
		return self.name

	def write(self, txt):
		with open(self.textfile, "a") as f:
			f.write(txt) # python will convert \n to os.linesep

	def read(self):
		with open(self.textfile) as f:
			content = f.readlines()
			print content
			return content

	def parse(self):
		data = []
		line_measures = []
		line_logs = []
		start_time = ''
		with open(self.textfile) as f:
			content = f.readlines()
			is_start = 0
			for line in content:	# iterates through lines and checks header
				if line[0] == defines.LOG_HEADER:
					line_logs.append(line[1:])
					if 'Aquisition has started' in line:
						is_start = 1
					else:
						is_start = 0
				elif line[0] == defines.MEASUREMENT_HEADER:
					line_measures.append(line[1:])
					if is_start == 1:
						start_time = line[1:]
						start_time = start_time[:4] #
						print '\n\nStart time: '
						print start_time					
						globals()['start_time'] = start_time # sets global variable
						is_start = 0
					is_start = 0

		pairs = [] # next, will not be pairs, but trios, and so on, depending on the number of sensors

		for line in line_measures:
			[pairs.append(x.strip()) for x in line.split(';')]

		m_times = []
		m_lint = []

		for item in pairs:
			is_start = item.partition(',');
			m_times.append(is_start[0])
			m_lint.append(is_start[2])

		start_t = float(start_time)
		time_values = [(float(x)-start_t)/1000 for x in m_times] # converts values to float and for X, removes offset and divides by 1000 (data in ms)
		lint_values = [float(y) for y in m_lint]

		data = [time_values, lint_values] #data are float values

		return data

		#print '\n\nTime and values'
		#print m_times
		#print m_lint
