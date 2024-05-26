from flask import Flask,render_template, request, jsonify 
import pyautogui
from datetime import datetime

app = Flask(__name__,template_folder="templates") 

@app.route("/") 
def hello(): 
	return render_template('index.html') 

@app.route('/process-data', methods=['POST']) 
def process_data(): 
	data = request.json['data'] 
	# result = sum(data) 
	print(data)
	xdisp = float(data["x"])
	ydisp = float(data["y"])
	deltax = xdisp
	deltay = ydisp
	if(abs(deltax)<1): 
		deltax=0
	if(abs(deltay)<1):
		deltay=0
	pyautogui.moveRel((deltax), 0, duration=0.1)
	# print(f'x: {xdisp} deltax = {deltax} y: {ydisp} deltay: {-deltay}')

	return jsonify({'result': data}) 

if __name__ == '__main__': 
	app.run(debug=True) 
