# Imports
import numpy as np
import pandas as pd
import os
import re
from datetime import date, timedelta, datetime

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from utilities import *

# Always add when using pandas
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 100)

def convert(input_path, constants):

# Setup
	# Constants of individual
	name = constants['name']
	year_first = datetime.strptime(constants['date_start'], '%Y-%m-%d').year
	date_start = datetime.strptime(constants['date_start'], '%Y-%m-%d')
	january_switch_count = False
	
	# Constants of rota format
	rota_datetime_format = '%d-%b'
	dates_letnum = 1 #the column/row which has the dates in it
	entries_to_exclude = ['OFF', 'X', 'x', 'BH', 'A/L', 'AL']
	
# Main
	# Setting up list of sheet names
	sheet_names = pd.ExcelFile(input_path).sheet_names

# V Would normally be later on, but has to be before the sheet_name loop V
	if 'year_first' in locals():
		year_to_replace = year_first

	# Setting up dates_dict - a dictionary of lists - to append entries to later
	dates_dict = {}
	dates_dict['start date'] = []
	dates_dict['end date'] = []
	dates_dict['subject'] = []
	dates_dict['all day event'] = []
# ^ Would normally be later on, but has to be before the sheet_name loop ^

	# Loop through each sheet
	for sheet in sheet_names:
		# Read file
		df = pd.read_excel(input_path, sheet_name=sheet, header=None)

		# Match indexes and headers to excel
		df.columns = [ColNum2ColName(i+1) for i, v in enumerate(df.columns)]
		df.index = pd.Series(df.index).shift(-1).fillna(len(df.index)).astype(int)

		# Define number of rows to read: If rota is horizontal, then specify nrows for pd.read_excel. If rota is vertical, then nrows=None	
		names_col = 'A'
		names_values = df[names_col].values.tolist()
		for i in range(0, len(names_values)):
			if i not in [0, 1]:
				if names_values[i] == 'Total Juniors':
					nrows = i
					break

		# Load again but only nrows number of rows
		df = pd.read_excel(input_path, sheet_name=sheet, nrows=nrows, header=None)

		# Match indexes and headers to excel
		df.columns = [ColNum2ColName(i+1) for i, v in enumerate(df.columns)]
		df.index = pd.Series(df.index).shift(-1).fillna(len(df.index)).astype(int)
	
		# Drop hidden rows
		hidden_row_indexes = find_hidden_row_indexes(input_path)
		df.drop(hidden_row_indexes, inplace=True)

		# Change into a vertical rota with dates as rows and columns as 'dates' and 'person'
		df = pd.DataFrame.transpose(df)

		# Rename 'Date' column and change header columns to the names
		df[dates_letnum]['A'] = 'Date'
		df.columns = df.loc[names_col].values.tolist()
		df.drop('A', inplace=True)

		if name in df.columns.tolist():
			# Filter columns (only dates column and person's rota entries column should remain at the end)
			df = df[['Date', name]]

			# Filter rows (only include rows with entries to be included)
			df = df[pd.notnull(df['Date'])]

			# Making dates and rota_list lists
			dates = []
			for i, v in df['Date'].iteritems():
				if isinstance(v, int):
					v = v.to_pydatetime()
				elif isinstance(v, str):
					v = datetime.strptime(v, rota_datetime_format)
				dates.append(v)
			rota_list = df[name].values.tolist()

			for i, rota_entry in enumerate(rota_list):
				date = dates[i]

					
				# If anywhere from the second date onwards the month is January, and it hasn't been done before already, then year_first should be increased by one. This is to accommodate rotas crossing December into January
				if (sheet_names.index(sheet) == 0 and i >= 1) or (sheet_names.index(sheet) >=1):
					if date.month == 1 and january_switch_count == False:
						year_to_replace += 1
						january_switch_count = True

				# The year should be made to be the year inputted by the user, or the next year if January has been crossed
				date = date.replace(year=year_to_replace)
				date_string = datetime.strftime(date, '%d/%m/%Y')

				if date < date_start:
					continue

				if (isinstance(rota_entry, str) and rota_entry not in ['OFF', 'X', 'BH', 'A/L', 'AL']):
						subject = rota_entry
						dates_dict['subject'].append(subject)
						dates_dict['start date'].append(date.strftime(f'%d/%m/%Y'))
						dates_dict['end date'].append( (date+timedelta(days=1)).strftime('%d/%m/%Y') )
						dates_dict['all day event'].append('True')


	df_result = pd.DataFrame(dates_dict)

	return df_result

if __name__ == '__main__':
	print(convert('../../../user_input/input_brighton_resp.xlsx', {
		'name': 'Shruti Dorai',
		'date_start': '2018-08-02'}))