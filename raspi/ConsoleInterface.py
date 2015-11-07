import os

# Get parameters from console
height, width = os.popen('stty size', 'r').read().split()
height = int(height)
width = int(width)

class ConsoleInterface(object):
    """A class that makes the CLI."""
    def __init__(self):
        self.width = width
        self.height = height
        self.col_num = 8

    def printRow(self, row):
        #col_width = max(len(word) for word in row) + 2
        col_width = self.width/self.col_num;
        print ''.join(word[0:8].ljust(col_width) for word in row) #joins columns truncating at 8 chars.

    def printCenteredWithSymbol(self, text, symbol):
        # prints text in the center of a terminal surrounded by repetitions of symbol (multiple characters accepted)
        if text == '':
            to_print = symbol * ((self.width - len(text))/(len(symbol)))
        else:
            to_print = symbol * ((self.width - len(text) - 2)/(2*len(symbol))) + ' ' + text + ' ' + symbol * ((self.width - len(text) - 1)/(2*len(symbol)))
        print to_print
        return to_print

    def initInterface(self):
        std_row = ['AAAAAAAA','BBBBBBBB','CCCCCCCC','DDDDDDDD','EEEEEEEE','FFFFFFF','GGGGGGGG','HHHHHHHH']
        empty_row = ['','','','','','','','']
        data_row = ['','','','','','','','']

        os.system('clear')
        self.printCenteredWithSymbol('', '-')
        self.printCenteredWithSymbol('Welcome to OpBox v0.0', '* ')
        self.printCenteredWithSymbol('', '-')
        self.printRow(empty_row)
        self.printRow(std_row)
        self.printRow(empty_row)
        self.printRow(std_row)
        self.printRow(empty_row)
        self.printRow(std_row)

#Test code


