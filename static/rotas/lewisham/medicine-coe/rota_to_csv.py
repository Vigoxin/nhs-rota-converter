# Imports
import numpy as np
import pandas as pd
import os
from datetime import datetime as dt
import datetime
import re

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from utilities import *

# Always add when using pandas
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 2000)
pd.set_option('display.width', 150)

# https://stackoverflow.com/questions/34156830/leave-dates-as-strings-using-read-excel-function-from-pandas-in-python
def undate(x):
    if pd.isnull(x):
        return x
    try:
        return x.strftime('%d/%m/%Y')
    except AttributeError:
        return x
    except Exception:
        raise

def convert(input_path, constants):

# Setup

	# Constants of individual
	row_number = int(constants['row_number'])
	date_start = dt.strptime(constants['date_start'], '%Y-%m-%d')
	date_end = dt.strptime(constants['date_end'], '%Y-%m-%d')

	# Constants of rota format
	rota_datetime_format = '%d/%m/%Y'
	dates_letnum = int(constants['dates_row_num']) #the column/row which has the dates in it
	entries_to_exclude = ['ZERO', np.nan, datetime.time(0,0,0)]



# Main
	# Read file
	df = pd.read_csv(input_path, header=None)

	# Match indexes and headers to excel
	df.columns = [ColNum2ColName(i+1) for i, v in enumerate(df.columns)]
	df.index = pd.Series(df.index).shift(-1).fillna(len(df.index)).astype(int)

	# Change into a vertical rota with dates as rows and columns as 'dates' and 'person'
	df = pd.DataFrame.transpose(df)

	# Rename 'Date' column
	df = df.rename(columns={dates_letnum: 'Date'})

	# Filter columns (only dates column and person's rota entries column should remain at the end)
	df = df[['Date', row_number]]

	# Filter rows (only include rows with entries to be included)
	df = df[pd.notnull(df['Date'])] #remove rows where the date column is null

		# Change all dates into strings
	df['Date'] = df['Date'].apply(lambda x: x.strftime('%d/%m/%Y') if isinstance(x,datetime.datetime) else x)

	# reset index
	df.reset_index(inplace=True, drop=True)
	df.reset_index(inplace=True, drop=True)
	
	
	# Filter based on date range selected by user
		# Remove date entries which say 'AL TOTAL' or 'SL TOTAL' etc
	df = df[df['Date'].apply(lambda x: not re.search('[a-zA-Z]', x))]
		# Convert all to datetime
	df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y")
	# df['Date'] = pd.to_datetime(df['Date'])
		# Actual filtering
	df = df[df['Date'].apply(lambda x: x >= date_start and x <= date_end)]

	# Making dates and rota_list lists
	dates = []
	for i, v in df['Date'].iteritems():
		# v = v.to_pydatetime()
		dates.append(v)
	rota_list = df[row_number].values.tolist()

	# Setting up dates_dict - a dictionary of lists - to append entries to later
	dates_dict = {}
	dates_dict['start date'] = []
	dates_dict['end date'] = []
	dates_dict['subject'] = []
	dates_dict['all day event'] = []

	for i, entry in enumerate(rota_list):
		date = dates[i]
		date_string = dt.strftime(date, '%d/%m/%Y')

		if entry in entries_to_exclude: # If entry is not to be added to output calendar - skip and don't add to entry list
			continue				
		else:						# If entry is something to be added
			subject = entry			# then make the subject whatever it says and add it to the final list
		dates_dict['start date'].append(date_string)
		dates_dict['end date'].append( (date+datetime.timedelta(days=1)).strftime('%d/%m/%Y') )
		dates_dict['subject'].append(subject)
		dates_dict['all day event'].append('True')

	df_result = pd.DataFrame(dates_dict)
	return df_result

if __name__ == '__main__':
	print(os.getcwd())
	# print(convert('../../../user_input/input_lewisham_medicine.csv', {
	# 	'sheet_num': '3',
	# 	'row_number': '20',
	# 	'dates_row_num': '3',
	# 	'date_start': '2021-08-04',
	# 	'date_end': '2021-11-30'
	# }))
	# print(convert('../../../user_input/input_lewisham_medicine_2.csv', {
	# 	'sheet_num': '2',
	# 	'row_number': '6',
	# 	'dates_row_num': '4',
	# 	'date_start': '2021-12-01',
	# 	'date_end': '2022-04-05'
	# }))
	print(convert('../../../user_input/input_lewisham_medicine_3.csv', {
		'sheet_num': '4',
		'row_number': '14',
		'dates_row_num': '2',
		'date_start': '2022-04-06',
		'date_end': '2022-08-02'
	}))