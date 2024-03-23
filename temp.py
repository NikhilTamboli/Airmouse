import dash
from dash.dependencies import Output, Input
from dash import dcc, html, dcc
from datetime import datetime
import json
import plotly.graph_objs as go
from collections import deque
from flask import Flask, request
import pyautogui

import socket
hostname = socket.gethostname()
print(socket.gethostbyname(hostname))

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

MAX_DATA_POINTS = 1000
UPDATE_FREQ_MS = 100

time = deque(maxlen=MAX_DATA_POINTS)
accel_x = deque(maxlen=MAX_DATA_POINTS)
accel_y = deque(maxlen=MAX_DATA_POINTS)
accel_z = deque(maxlen=MAX_DATA_POINTS)

app.layout = html.Div(
	[
		dcc.Markdown(
			children="""
			# Live Sensor Readings
		"""
		),
		# dcc.Graph(id="live_graph"),
		# dcc.Interval(id="counter", interval=UPDATE_FREQ_MS),
	]
)


@app.callback(Output("live_graph", "figure"), Input("counter", "n_intervals"))

def update_graph(_counter):
	data = [
		go.Scatter(x=list(time), y=list(d), name=name)
		for d, name in zip([accel_x, accel_y, accel_z], ["X", "Y", "Z"])
	]

	graph = {
		"data": data,
		"layout": go.Layout(
			{
				"xaxis": {"type": "date"},
				"yaxis": {"title": "Acceleration ms<sup>-2</sup>"},
			}
		),
	}
	if (
		len(time) > 0
	):  #  cannot adjust plot ranges until there is at least one data point
		graph["layout"]["xaxis"]["range"] = [min(time), max(time)]
		graph["layout"]["yaxis"]["range"] = [
			min(accel_x + accel_y + accel_z),
			max(accel_x + accel_y + accel_z),
		]

	return graph

@server.route("/data", methods=["POST"])
def data():  # listens to the data streamed from the sensor logger

	if str(request.method) == "POST":
		data = json.loads(request.data)
		js = data['payload']
		# print(js)
		d = js.pop()
		ts = datetime.fromtimestamp(d["time"] / 1000000000)
		if len(time) == 0 or ts > time[-1]:
			xac = d["values"]["x"]
			yac = 9.80665-d["values"]["z"]
			if(abs(xac)<0.5):
				xac=0
			if(abs(yac)<0.5):
				yac=0
			pyautogui.moveRel((xac), -(yac), duration=1)
			print(f'x: {xac} y: {yac}')
			time.append(ts)			
		            		
	return "success"


if __name__ == "__main__":
	app.run_server(port=8000, host="0.0.0.0")