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
pd.set_option('display.max_rows', 200)
pd.set_option('display.width', 150)


def convert(input_path, constants):

# Setup

	# Constants of individual
	row_number = int(constants['row_number'])

	# Constants of rota format
	rota_datetime_format = '%d/%m/%Y'
	dates_letnum = 3 #the column/row which has the dates in it
	entries_to_exclude = ['Leave', 'Off', 'Zero', np.nan, datetime.time(0,0,0), 'BH']



# Main
	# Read file
	df = pd.read_excel(input_path, header=None)

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

	# reset index
	df.reset_index(inplace=True, drop=True)
	df.reset_index(inplace=True, drop=True)

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
	print(convert('../../../user_input/input_ashford_st_peters_medicine.xlsx', {
		'row_number': '120',
		# 'date_start': '2021-08-04',
		'date_start': '2021-08-09',
		# 'date_end': '2022-02-01'
		'date_end': '2022-01-27'
	}))