import os
from table import Table

# Get parameters from console
height, width = os.popen('stty size', 'r').read().split()
height = int(height)
width = int(width)

class ConsoleInterface(object):
    """A class that makes the CLI."""
    def __init__(self, table):
        self.width = width
        self.height = height
        self.col_num = 8
        self.table = table

    def print_row(self, row):
        #col_width = max(len(word) for word in row) + 2
        col_width = self.width/self.col_num;
        print ''.join(word[0:col_width-2].ljust(col_width) for word in row) #joins columns truncating at 8 chars.

    def rprint_row(self, row):
        #col_width = max(len(word) for word in row) + 2
        col_width = self.width/self.col_num;
        print ''.join(word[0:col_width-2].rjust(col_width) for word in row) #joins columns truncating at 8 chars.

    def cprint_row(self, row):
        #col_width = max(len(word) for word in row) + 2
        col_width = self.width/self.col_num;
        print ''.join(word[0:col_width-2].center(col_width) for word in row) #joins columns truncating at 8 chars.

    def print_row_entire_words(self, row):
        #col_width = max(len(word) for word in row) + 2
        col_width = self.width/self.col_num;
        print ''.join(word.ljust(col_width) for word in row) #joins columns NOT truncating

    def print_centered_with_symbol(self, text, symbol):
        # prints text in the center of a terminal surrounded by repetitions of symbol (multiple characters accepted)
        if text == '':
            text = ' '
            to_print = symbol * ((self.width - len(text))/(len(symbol)))
        else:
            to_print = symbol * ((self.width - len(text) - 2)/(2*len(symbol))) + ' ' + text + ' ' + symbol * ((self.width - len(text) - 1)/(2*len(symbol)))
        print to_print
        return to_print

    def new_line(self):
        empty_row = ['','','','','','','','']
        self.print_row(empty_row)

    def draw_table(self):
        pass

    def init_interface(self):
        std_row = ['AAAAAAAA','BBBBBBBB','CCCCCCCC','DDDDDDDD','EEEEEEEE','FFFFFFF','GGGGGGGG','HHHHHHHH']
        data_row = ['','','','','','','','']

        os.system('clear')
        self.print_centered_with_symbol('', ' ')
        self.print_centered_with_symbol('Welcome to OpBox v0.0', ' ')
        self.print_centered_with_symbol('contact@opbox.org', ' ')
        self.new_line() 
        self.print_centered_with_symbol('', '=')
        self.cprint_row(['Date: ','12/11/15','','Start time: ','13:34:33','','Routine: ','03A'])
        self.print_centered_with_symbol('', '=')
        self.new_line()
        self.print_centered_with_symbol('MEASUREMENTS', '  .  ')
        self.new_line()
        self.cprint_row(['Time','',   'Temp[oC]','','FBar','','LInt[lx]',''])
        self.cprint_row(['13:34:33','','23.3','','20.2','','56',''])
        self.cprint_row(['13:34:33','','23.2','','6.7','','56',''])
        self.cprint_row(['13:34:34','','23.3','','0.0','','59',''])
        self.new_line()
        self.new_line()
#Test code


