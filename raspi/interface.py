import os

COL_NUM = 8

# Get parameters from console
height, width = os.popen('stty size', 'r').read().split()
height = int(height)
width = int(width)

# Standards for printing (row by row)
std_row = ['AAAAAAAA','BBBBBBBB','CCCCCCCC','DDDDDDDD','EEEEEEEE','FFFFFFF','GGGGGGGG','HHHHHHHH']
empty_row = ['','','','','','','','']
data_row = ['','','','','','','','']

def printRow(row):
	#col_width = max(len(word) for word in row) + 2
	col_width = width/COL_NUM;
	print "".join(word.ljust(col_width) for word in row)

def printCenteredWithSymbol(text, symbol):
	# prints text in the center of a terminal surrounded by repetitions of symbol (multiple characters accepted)
	if text == '':
		to_print = symbol * ((width - len(text))/(len(symbol)))
	else:
		to_print = symbol * ((width - len(text) - 2)/(2*len(symbol))) + ' ' + text + ' ' + symbol * ((width - len(text) - 1)/(2*len(symbol)))
	print to_print
	return to_print

def initInterface():
	os.system('clear')
	printCenteredWithSymbol('', '-')
	printCenteredWithSymbol('Welcome to OpBox v0.0', '* ')
	printCenteredWithSymbol('', '-')
	printRow(empty_row)
	printRow(std_row)
	printRow(empty_row)
	printRow(std_row)
	printRow(empty_row)
	printRow(std_row)



#### Code itself ####
initInterface()