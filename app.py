#  --------- IMPORTS ---------

from flask import Flask, render_template, request, send_file
from flask_log_request_id import RequestID, current_request_id
from werkzeug.utils import secure_filename
from copy import deepcopy
import os
basedir = os.path.abspath(os.path.dirname(__file__))

#  --------- SETUP ---------

# initialise app
app = Flask(__name__, template_folder='./', static_folder='./static')

# Set up RequestID
RequestID(app)

# Import dict of all possible rota types
from rotas import rotas
from rotas import nice_name_dict
from rotas import nice_name_dict_reversed

# remove functions (non-serialisable) from rotas dict, before sending rotas into templates (as part of pd) as a variable
rotas_temp = deepcopy(rotas)
for hosp in rotas_temp:
	for specialty in rotas_temp[hosp]:
		pop_list = ['converter']
		for to_pop in pop_list:
			rotas_temp[hosp][specialty].pop(to_pop, None)
pd = {
	'rotas': rotas_temp,
	'nice_name_dict': nice_name_dict,
	'nice_name_dict_reversed': nice_name_dict_reversed
}

def nastyToNice(nasty):
	return pd['nice_name_dict'][nasty]

def niceToNasty(nice):
	return pd['nice_name_dict_reversed'][nice]

# Make input and output folders if they don't exist already
folders = ['static/input', 'static/output']
for folder in folders:
	if not os.path.isdir(folder):
		os.mkdir(folder)




#  --------- ROUTES ---------

@app.route('/')
def before():
	return render_template('templates/home.html', pd=pd)

# Home route
@app.route('/nhsrotaconverter/')
def home():
	return render_template('templates/home.html', pd=pd)

@app.route('/nhsrotaconverter/upload/<hospital>/<specialty>')
def upload(hospital, specialty):
	return render_template('templates/upload.html', hospital=hospital, specialty=specialty, pd=pd)

@app.route('/nhsrotaconverter/expand')
def expand():
	return render_template('templates/expand.html', pd=pd)

@app.route('/nhsrotaconverter/about')
def about():
	return render_template('templates/about.html', pd=pd)

@app.route('/nhsrotaconverter/convert/<hospital>/<specialty>', methods=['POST'])
def convert_route(hospital, specialty):
	
	# Function to check if file extension is only one of a few (can't allow html files - xss attacks)
	ALLOWED_EXTENSIONS = ['.xlsx', '.xls', '.csv', '.docx', '.doc']
	def allowed_file(filename):
		return '.' in filename and os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

	# gets the file and its extension
	file = request.files['rota']
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		fileext = os.path.splitext(filename)[1]

		# gets request ID so that each file to upload and process has a unique name
		req_id = current_request_id()
		input_path = f'static/input/input_{req_id}{fileext}'
		output_path = f'static/output/output_{req_id}.csv'

		# gets constants from request form data
		constants = request.form.to_dict()

		# Saves file as a unique name with a req id and the same extension it was uploaded as
		file.save(input_path)

		try:			
			# Gets the converter function for the specific rota type
			convert = rotas[hospital][specialty]['converter']
			
			# Converts the file and saves it to unique name
			df_result = convert(input_path, constants)
			df_result.to_csv(output_path, index=False)

			# stores the file to be sent as a download attachment
			to_send = send_file(output_path, attachment_filename='converted_rota.csv', as_attachment=True)	
		except:
			to_send = 'Sorry, an error occurred. Please make sure you have followed the instructions. Please email vignesh.dhileepan@gmail.com for help'


		# Deletes both the input and output files if they exist
		for file_to_delete in [input_path, output_path]:
			if os.path.isfile(file_to_delete):
				os.remove(file_to_delete)

		# Sends the file to be sent as a download attachment
		return to_send


if __name__ == '__main__':
	app.run(port=5001, debug=True)