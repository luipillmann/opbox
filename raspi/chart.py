import plotly.plotly as py
import plotly.graph_objs as go

class Chart(object):
	"""A class that makes charts."""
	def __init__(self, name, chart_type, data):
		self.name = name
		self.type = chart_type
		self.data = data
	
	def plot(self):
		print 'Plotting chart...'
		trace1 = go.Scatter(
			x=self.data[0],
			y=self.data[1],
			mode='markers'
		)
		data = [trace1]
		if self.name == '':
			self.name = 'default_plot'
		plot_url = py.plot(data, filename=self.name)


		#time.sleep(2) # wait for Arduino