"""
Interface based on 8 coloumns

Column width and word length parametrized by consoles dimension (2 chars for padding)
    Recommend word max. length: 8 chars for 80-column console

init_interface prints header (still hardcoded)
print_row, cprint_row, rprint_row print row aligned to the left, center and right, respectively.
print_centered_with_symbol is useful to fill lines with symbols and, optionally, a title.
draw_table prints table of values from the table binded in instantiation

"""

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
        self.print_centered_with_symbol('Skinner Box Data Aquisition', '  .  ')
        self.new_line()
        self.print_centered_with_symbol('', '-')
        self.cprint_row(['Time','',   'Temp[oC]','','FBar[N]','','LInt[lx]',''])
        self.print_centered_with_symbol('', '-')
        for row in self.table.rows:
            self.cprint_row([row[0],'',row[1],'',row[2],'',row[3],''])            

    def init_interface(self):
        os.system('clear')
        self.print_centered_with_symbol('', ' ')
        self.print_centered_with_symbol('Welcome to OpBox v0.1', ' ')
        self.print_centered_with_symbol('contact@opbox.org', ' ')
        self.new_line() 
        self.print_centered_with_symbol('', '=')
        self.cprint_row(['Date: ','12/11/15','','Start time: ','13:34:33','','Routine: ','03A'])
        self.print_centered_with_symbol('', '=')
        self.new_line()

    def show_menu(self):
        op = raw_input('Do you want to start the experiment? (y/n) ')
        return op

    def setup_interface(self):
        self.print_centered_with_symbol('TEST SETUP:', '  -  ')


    def update_interface(self):
        self.init_interface()
        self.draw_table()
        


