#  --------- IMPORTS ---------

from flask import Flask, render_template, request, send_file, redirect, Response, make_response
from flask_log_request_id import RequestID, current_request_id
from werkzeug.utils import secure_filename
from copy import deepcopy
from pandas import read_excel
import os
basedir = os.path.abspath(os.path.dirname(__file__))

#  --------- SETUP ---------

# initialise application
application = Flask(__name__, template_folder='./', static_folder='./static')

# Set up RequestID
RequestID(application)

# Import dict of all possible rota types
from rotas import rotas
from rotas import nice_name_dict
from rotas import nice_name_dict_reversed

# remove functions (which are non-serialisable) from rotas dict, before sending rotas into templates (as part of pd) as a variable
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

# Home route
@application.route('/')
def home():
	return render_template('templates/home.html', pd=pd)

@application.route('/upload/<hospital>/<specialty>')
def upload(hospital, specialty):
	return render_template('templates/upload.html', hospital=hospital, specialty=specialty, pd=pd)

@application.route('/expand')
def expand():
	return render_template('templates/expand.html', pd=pd)

@application.route('/about')
def about():
	return render_template('templates/about.html', pd=pd)

@application.route('/error')
def error():
	return render_template('templates/error_page.html', pd=pd)

@application.route('/convert/<hospital>/<specialty>', methods=['POST'])
def convert_route(hospital, specialty):
	to_send = redirect('/error')

	# Function to check if file extension is only one of a few (can't allow html files - xss attacks)
	ALLOWED_EXTENSIONS = ['.xlsx', '.xls', '.csv', '.docx', '.doc']
	def allowed_file(filename):
		return '.' in filename and os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

	# gets the file and its extension
	file = request.files.get('rota')
	if file and allowed_file(file.filename):		

		# gets constants from request form data
		constants = request.form.to_dict()
		print(constants)

		try:
			# Gets the converter function for the specific rota type
			convert = rotas[hospital][specialty]['converter']
			
			# Reads the file directly from the post request into a pandas dataframe, 
			# then converts the file
			df_result = convert(file, constants)
			to_send = Response(df_result.to_csv(index=False), mimetype="text/csv", headers={
				"Content-disposition": "attachment; filename=converted_rota.csv"
			})
		except Exception as e:
			print(e)
			pass

	# Sends the file to be sent as a download attachment
	return to_send


if __name__ == '__main__':
	application.run(port=8000, debug=True)
