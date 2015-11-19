import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls

tls.set_credentials_file(username='luipillmann', api_key='k0aql2lhru')


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
			y=self.data[3],
			mode='markers'
		)

		trace2 = go.Scatter(
			x=self.data[0],
			y=self.data[1],
			mode='markers'
		)
		data = [trace1, trace2]
		if self.name == '':
			self.name = 'default_plot'
		plot_url = py.plot(data, filename=self.name)

	def plot_mult(self):
		""" Chart with multiple Y axes """
		trace1 = go.Scatter(
		    x=self.data[0],
			y=self.data[1],
		    name='Temperature'
		)
		trace2 = go.Scatter(
		    x=self.data[0],
			y=self.data[2],
		    name='Pressing force (bar)',
		    yaxis='y2'
		)
		trace3 = go.Scatter(
		    x=self.data[0],
			y=self.data[3],
		    name='Light intensity',
		    yaxis='y3'
		)
		# trace4 = go.Scatter(
		#     x=[5, 6, 7],
		#     y=[400000, 500000, 600000],
		#     name='yaxis4 data',
		#     yaxis='y4'
		# )
		data = [trace1, trace2, trace3]#, trace4]
		layout = go.Layout(
		    title='OpBox: [' + self.name +']',
		    width=1200,
		    xaxis=dict(
		        domain=[0.3, 0.7]
		    ),
		    yaxis=dict(
		        title='Temperature [oC]',
		        titlefont=dict(
		            color='#1f77b4'
		        ),
		        tickfont=dict(
		            color='#1f77b4'
		        )
		    ),
		    yaxis2=dict(
		        title='Pressing force (bar) [N]',
		        titlefont=dict(
		            color='#ff7f0e'
		        ),
		        tickfont=dict(
		            color='#ff7f0e'
		        ),
		        anchor='free',
		        overlaying='y',
		        side='left',
		        position=0.15
		    ),
		    yaxis3=dict(
		        title='Light intensity [lux]',
		        titlefont=dict(
		            color='#2ca02c'
		        ),
		        tickfont=dict(
		            color='#2ca02c'
		        ),
		        anchor='x',
		        overlaying='y',
		        side='right'
		    )#,
		    # yaxis4=dict(
		    #     title='yaxis5 title',
		    #     titlefont=dict(
		    #         color='#9467bd'
		    #     ),
		    #     tickfont=dict(
		    #         color='#9467bd'
		    #     ),
		    #     anchor='free',
		    #     overlaying='y',
		    #     side='right',
		    #     position=0.85
		    # )
		)
		fig = go.Figure(data=data, layout=layout)
		plot_url = py.plot(fig, filename=self.name)
		print '\nAccess the plot in the link below: '
		print plot_url
