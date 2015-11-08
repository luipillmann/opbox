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

	def get_start_time(self):
		start_time = ''
		with open(self.textfile) as f:
			content = f.readlines()
			is_start = 0
			for line in content:	# iterates through lines and checks header
				if line[0] == defines.LOG_HEADER:
					if 'Aquisition has started' in line:
						is_start = 1
					else:
						is_start = 0
				elif line[0] == defines.MEASUREMENT_HEADER:
					if is_start == 1: # saves time value from this line as start time as detected above
						start_time = line[1:]
						start_time = start_time[:4] 
						globals()['start_time'] = start_time # sets global variable
						is_start = 0
						return float(start_time)
					is_start = 0


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
					line_measures.append(line)
					if is_start == 1: # saves time value from this line as start time as detected above
						start_time = line[1:]
						start_time = start_time[:4] 
						globals()['start_time'] = start_time # sets global variable
						is_start = 0
					is_start = 0

		values = [] # next, will not be pairs, but trios, and so on, depending on the number of sensors

		for line in line_measures:
			[values.append(x.strip()) for x in line.split(',')]
		
		m_time = []
		m_temp = []
		m_fbar = []
		m_lint = []

		for item in values:
			if item[0] == defines.MEASUREMENT_HEADER:
				m_time.append(item[1:])
			elif item[0] == defines.TEMPERATURE_HEADER:
				m_temp.append(item[1:])
			elif item[0] == defines.FORCE_BAR_HEADER:
				m_fbar.append(item[1:])
			elif item[0] == defines.LIGHT_HEADER:
				m_lint.append(item[1:])

		# Processes values to float. Time to seconds
		start_t = float(start_time)
		time_values = [(float(x)-start_t)/1000 for x in m_time] # converts values to float and for X, removes offset and divides by 1000 (data in ms)
		temp_values = [float(y) for y in m_temp]
		fbar_values = [float(y) for y in m_fbar]
		lint_values = [float(y) for y in m_lint]
		
		data = [time_values, temp_values, fbar_values, lint_values] #data are float values

		return data

		#print '\n\nTime and values'
		#print m_times
		#print m_lint
