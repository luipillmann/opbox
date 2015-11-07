"""
interface_test.py

Test for the interface. How it works:
	A class ConsoleInterface to manage operations in the screen (printing stuff)
	Another class Table with the data to be printed

	The test uses 4 vectors: 1 with time values + 3 with sensors
		Print layout is hardcoded inside ConsoleInterface.init_interface and ConsoleInterface.draw_table
	build_rows takes these 4 vectors and turn into rows matching values with same index (function has to be moved somewhere else)

	Data is added to 'data' object which is binded to the interface (done in 'console''s instantiation)
	Then, draw_table is called to append the table values to the interface (later, this method may be called to refresh screen)
	Values and header info is are hardcoded here and in ConsoleInterface declaration, respectively.

"""

from table import Table
from interface import ConsoleInterface

data = Table('data') 

time = ['19:00:32', '19:00:32', '19:00:33', '19:00:34']
temp = ['23.0', '23.0', '23.0', '23.0']
fbar = ['0.0', '12.0', '87.2', '0.0']
ilux = ['60.1', '69.1', '62.1', '62.1']

console = ConsoleInterface(data) # binds data table to interface object
console.init_interface() # prints header

def build_rows(ptime, ptemp, pfbar, pilux):
	rows = []
	if len(ptime) == len(ptemp) == len(pfbar) == len(pilux):
		for x, val in enumerate(ptime):
			rows.append([ptime[x], ptemp[x], pfbar[x], pilux[x]])
	else:
		print 'ERROR: Data values not the same lenght.'

	return rows


data.add_rows(build_rows(time, temp, fbar, ilux))

console.draw_table()

var = raw_input()




