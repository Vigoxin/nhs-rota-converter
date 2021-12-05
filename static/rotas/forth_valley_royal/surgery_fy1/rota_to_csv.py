# Imports
import numpy as np
import pandas as pd
import os
from datetime import date, timedelta, datetime
import datetime as dt

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from utilities import *

# Always add when using pandas
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', None)

def convert(input_path, constants):

# Setup
	# Constants of individual
	col_letter = constants['column_letter'].upper()
	date_start = datetime.strptime(constants['date_start'], '%Y-%m-%d')
	date_end = datetime.strptime(constants['date_end'], '%Y-%m-%d')

	# Constants of rota format
	rota_datetime_format = '%d/%m/%y'
	dates_letnum = 'B' #the column/row which has the dates in it
	entries_to_exclude = ['Rest', 'Off', 'AL', 'A', 'A/L']

# Main
	# Read file
	df = pd.read_excel(input_path)

	# Match indexes and headers to excel
	df.columns = [ColNum2ColName(i+1) for i, v in enumerate(df.columns)]
	df.index = pd.Series(df.index).shift(-1).fillna(len(df.index)).astype(int)
	
	# Read again, but from the NAN row onwards
	a = df["A"][pd.isnull(df["A"])]
	df = pd.read_excel(input_path, header=a.index[0])

	# Match indexes and headers to excel
	df.columns = [ColNum2ColName(i+1) for i, v in enumerate(df.columns)]
	df.index = pd.Series(df.index).shift(-1).fillna(len(df.index)).astype(int)
	
	# # Drop hidden rows
	# hidden_row_indexes = find_hidden_row_indexes(input_path)
	# df.drop(hidden_row_indexes, inplace=True)

	# Change into a vertical rota with dates as rows and columns as 'dates' and 'person'

	# Rename 'Date' column
	df = df.rename(columns={dates_letnum: 'Date'})

	# Filter columns (only dates column and person's rota entries column should remain at the end)
	df = df[['Date', col_letter]]
	
	# Filter rows (only include rows with entries to be included)
	df = df[pd.notnull(df['Date'])]
	
	# Remove rows in the 'Date' column which are not dt.datetime (e.g. the rows in between the rotations)
	df = df[df["Date"].apply(lambda x: isinstance(x, dt.datetime))]

	# Remove rows in 'Date' column which aren't in the specified date range
	df = df[df['Date'].apply(lambda x: x <= date_end and x >= date_start)]

	# Making dates and rota_list lists
	dates = df["Date"].tolist()
	rota_list = df[col_letter].values.tolist()
	# print(df)
	# raise

	# Setting up dates_dict - a dictionary of lists - to append entries to later
	dates_dict = {}
	dates_dict['subject'] = []
	dates_dict['start date'] = []
	dates_dict['end date'] = []
	dates_dict['all day event'] = []

	if 'year_first' in locals():
		year_to_replace = year_first

	for i, rota_entry in enumerate(rota_list):
		date = dates[i]
		
		date_string = datetime.strftime(date, '%d/%m/%Y')
		
		if rota_entry.strip() not in entries_to_exclude: 					#If it's not already a zero day
			if isinstance(rota_entry, float) and pd.isnull(rota_entry): # If rota_entry is NaN
				is_weekend = False if date.weekday() < 5 else True
				if is_weekend:			#If it's a weekend, then don't add to the rota_entry final list
					continue
				elif not is_weekend:	#If it's a weekday, make the subject 'normal hours' and add to the final list
					subject = 'Normal hours'
			else:						# If rota_entry is not NaN
				subject = rota_entry			# then make the subject whatever it says and add it to the final list
			
			dates_dict['subject'].append(subject)
			dates_dict['start date'].append(date_string)
			dates_dict['end date'].append( (date+timedelta(days=1)).strftime('%d/%m/%Y') )
			dates_dict['all day event'].append('True')

	df_result = pd.DataFrame(dates_dict)
	return df_result

if __name__ == '__main__':
	df_result = convert('../../../user_input/input_forth_valley_royal_surgery.xlsx', {
		'column_letter': 'D',	
		'date_start': '2021-12-01',
		'date_end': '2022-04-05'
	})
	print(df_result)