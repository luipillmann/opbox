import time
import defines
from serial_ard import SerialArduino 
from file_handler import FileHandler
from chart import Chart
from table import Table
from interface import ConsoleInterface

txt = FileHandler('newtags')

txt.parse()