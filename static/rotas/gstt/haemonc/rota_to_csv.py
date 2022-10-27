# Imports
import numpy as np
import pandas as pd
import os
from datetime import date, timedelta, datetime

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from utilities import *

# Always add when using pandas
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 150)


def convert(input_path, constants):

# Setup
	# Constants of individual
	row_number = int(constants['row_number'])
	col_start = constants['col_start'].upper()
	col_end = constants['col_end'].upper()
	year_first = datetime.strptime(constants['date_start'], '%Y-%m-%d').year

	# Constants of rota format
	rota_datetime_format = '%d-%b'
	dates_letnum = 7 #the column/row which has the dates in it
	entries_to_exclude = ['OFF', np.nan, 'AL']

# Main
	# Read file
	df = pd.read_excel(input_path, header=None)

	# Match indexes and headers to excel
	df.columns = [ColNum2ColName(i+1) for i, v in enumerate(df.columns)]
	df.index = pd.Series(df.index).shift(-1).fillna(len(df.index)).astype(int)

	# Drop hidden rows
	hidden_row_indexes = find_hidden_row_indexes(input_path)
	df.drop(hidden_row_indexes, inplace=True)

	# Change into a vertical rota with dates as rows and columns as 'dates' and 'person'
	df = pd.DataFrame.transpose(df)

	# Drop unnecessary columns and rows
	df = df.iloc[:, 6:]
	df = df.iloc[3:]


	# Rename 'Date' column
	df = df.rename(columns={dates_letnum: 'Date'})

	# Filter columns (only dates column and person's rota entries column should remain at the end)
	df = df[['Date', row_number]]

	# Filter rows (only include rows with entries to be included)
	df = df[pd.notnull(df['Date'])] #remove rows where the date column is null
	df = df.loc[col_start:col_end, :]


	# Making dates and rota_list lists
	dates = []
	for i, v in df['Date'].iteritems():
		if isinstance(v, int):
			v = v.to_pydatetime()
		elif isinstance(v, str):
			v = datetime.strptime(v, rota_datetime_format)
		dates.append(v)
	rota_list = df[row_number].values.tolist()

	# Setting up dates_dict - a dictionary of lists - to append entries to later
	dates_dict = {}
	dates_dict['start date'] = []
	dates_dict['end date'] = []
	dates_dict['subject'] = []
	dates_dict['all day event'] = []

	if 'year_first' in locals():
		year_to_replace = year_first

	for i, entry in enumerate(rota_list):
		date = dates[i]

		# Determine year and replace year of date (if not already in date entries)
			# If anywhere from the second date onwards the month is January, and it hasn't been done before already, then year_first should be increased by one. This is to accommodate rotas crossing December into January
		if i >= 1:
			if date.month == 1 and dates[i-1].month == 12:
				year_to_replace += 1
			# The year should be made to be the year inputted by the user, or the next year if January has been crossed
		date = date.replace(year=year_to_replace)
		date_string = datetime.strftime(date, '%d/%m/%Y')

		if entry in entries_to_exclude: # If entry is NaN, of says X or OFF - skip and don't add to entry list
			continue				
		else:						# If entry is something to be added
			subject = entry			# then make the subject whatever it says and add it to the final list
		dates_dict['start date'].append(date_string)
		dates_dict['end date'].append( (date+timedelta(days=1)).strftime('%d/%m/%Y') )
		dates_dict['subject'].append(subject)
		dates_dict['all day event'].append('True')

	df_result = pd.DataFrame(dates_dict)
	return df_result

if __name__ == '__main__':
	print(os.getcwd())
	print(convert('../../../user_input/input_gstt_haemonc.xlsx', {
		'row_number': '11',
		'col_start': 'D',
		'col_end': 'DR',
		'date_start': '2022-12-07'}))