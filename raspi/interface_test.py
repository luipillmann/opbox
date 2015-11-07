from table import Table
from interface import ConsoleInterface

data = Table('data')

data.add_row(['19:00:32','23.0','12.0','20.1'])

console = ConsoleInterface(data)
console.init_interface()
console.draw_table()




