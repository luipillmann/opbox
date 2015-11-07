from table import Table
from interface import ConsoleInterface

data = Table('data')

time = ['19:00:32', '19:00:32', '19:00:33', '19:00:34']
temp = ['23.0', '23.0', '23.0', '23.0']
fbar = ['0.0', '12.0', '87.2', '0.0']
ilux = ['60.1', '69.1', '62.1', '62.1']

console = ConsoleInterface(data)
console.init_interface()

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




