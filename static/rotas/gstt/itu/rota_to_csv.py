# Imports
import numpy as np
import pandas as pd
import os
import math
from datetime import date, timedelta, datetime

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from utilities import *

# Always add when using pandas
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 100)

def convert(input_path, constants):

# Setup
	# Constants of individual
	col_letter = constants['column_letter'].upper()
	date_start = datetime.strptime(constants['date_start'], '%Y-%m-%d').date()
	date_end = datetime.strptime(constants['date_end'], '%Y-%m-%d').date()
	
	# Constants of rota format
	rota_datetime_format = '%Y/%m/%d'
	entries_to_exclude = ['O']

# Main
	# Read file
	df = pd.read_excel(input_path, header=None)

	# Match indexes and headers to excel
	df.columns = [ColNum2ColName(i+1) for i, v in enumerate(df.columns)]
	df.index = pd.Series(df.index).shift(-1).fillna(len(df.index)).astype(int)

	# Define number of rows to read: If rota is horizontal, then specify nrows for pd.read_excel. If rota is vertical, then nrows=None
	nrows = None

	# Load again but only nrows number of rows
	df = pd.read_excel(input_path, nrows=nrows, header=None)

	# Match indexes and headers to excel
	df.columns = [ColNum2ColName(i+1) for i, v in enumerate(df.columns)]
	df.index = pd.Series(df.index).shift(-1).fillna(len(df.index)).astype(int)
	
	# Drop hidden rows
	hidden_row_indexes = find_hidden_row_indexes(input_path)
	df.drop(hidden_row_indexes, inplace=True)

	# Change into a vertical rota with dates as rows and columns as 'dates' and 'person'
	# Process dates
	df["A"] = df["A"].fillna(method='ffill')
	df["B"] = df["B"][df["B"].notnull()].apply(lambda x: int(x.strip()[:-2] if pd.notnull(x) else x))
	df["A"] = df[df["B"].notnull()].apply(lambda x: x["A"].replace(day=int(x["B"])), axis=1)
	df["A"].iloc[0] = "Date"
	df.drop(["B", "C"], inplace=True, axis="columns")
	df.rename(columns = {'A':'Date'}, inplace = True)
	df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date

	# Filter columns (only dates column and person's rota entries column should remain at the end)
	df = df[['Date', col_letter]]
	
	# Filter rows (only include rows with entries to be included)
	df = df[pd.notnull(df['Date'])]
	df = df[df['Date'].apply(lambda x: x >= date_start and x <= date_end)]

	# Making dates and rota_list lists
	dates = []
	for i, v in df['Date'].iteritems():
		if isinstance(v, int):
			v = v.to_pydatetime()
		elif isinstance(v, str):
			v = datetime.strptime(v, rota_datetime_format)
		dates.append(v)
	
	rota_list = df[col_letter].values.tolist()


	# Setting up dates_dict - a dictionary of lists - to append entries to later
	dates_dict = {}
	dates_dict['start date'] = []
	dates_dict['end date'] = []
	dates_dict['subject'] = []
	dates_dict['all day event'] = []

	if 'year_first' in locals():
		year_to_replace = year_first

	for i, rota_entry in enumerate(rota_list):
		date = dates[i]

		# Determine year and replace year of date (if not already in date entries)

		date_string = datetime.strftime(date, '%d/%m/%Y')

		if rota_entry in entries_to_exclude or pd.isnull(rota_entry):
			continue
		else:						# If entry is not NaN
			subject = rota_entry			# then make the subject whatever it says and add it to the final list
		dates_dict['start date'].append(datetime.strftime(date, '%d/%m/%Y'))
		dates_dict['end date'].append( (date+timedelta(days=1)).strftime('%d/%m/%Y') )
		dates_dict['subject'].append(subject)
		dates_dict['all day event'].append('True')

	df_result = pd.DataFrame(dates_dict)
	return df_result

if __name__ == '__main__':
	df_result = convert('../../../user_input/input_gstt_itu.xlsx', {
		'column_letter': 'I',
		'date_start': '2022-08-03',
		'date_end': '2022-12-06'
	})
	print(df_result)