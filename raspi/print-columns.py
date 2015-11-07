data_to_print = [['a', 'b', 'c'], ['aaaaa', 'b', 'c'], ['a', 'bbbb', 'c']]

def printColumns(data):
	#col_width = max(len(word) for row in data for word in row) + 2  # padding
	col_width = width/COL_NUM;
	for row in data:
		print "".join(word.ljust(col_width) for word in row)