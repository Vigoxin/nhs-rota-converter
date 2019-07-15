# Imports
import numpy as np
import pandas as pd
import os
from datetime import date, timedelta, datetime
import re

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from utilities import *

# Always add when using pandas
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 150)


def convert(input_path, constants):

# Setup

	# Constants of individual
	row_number = int(constants['row_number'])
	date_start = datetime.strptime(constants['date_start'], '%Y-%m-%d')
	date_end = datetime.strptime(constants['date_end'], '%Y-%m-%d')
	year_first = date_start.year

	def custom_datetime_format_convert(d):
		groups = re.search('(\d+)\w+\s(\w+)', d).groups()
		return f"{groups[0].zfill(2)} {groups[1]} {year_first}"

	# Constants of rota format
	rota_datetime_format = '%d %B %Y'
	dates_letnum = 8 #the column/row which has the dates in it
	entries_to_exclude = ['X', 'OFF', 'ZERO', np.nan]



# Main
	# Read file
	df = pd.read_excel(input_path, header=None, sheet_name="HORIZONTAL VIEW")

	# Match indexes and headers to excel
	df.columns = [ColNum2ColName(i+1) for i, v in enumerate(df.columns)]
	df.index = pd.Series(df.index).shift(-1).fillna(len(df.index)).astype(int)

	# Define number of rows to read: If rota is horizontal, then specify nrows for pd.read_excel. If rota is vertical, then nrows=None
	names_col = df['D'].tolist()
	for i in range(0, len(names_col)):
		if i not in list(range(12)):
			if pd.isnull(names_col[i]):
				nrows = i
				break

	# Load again but only nrows number of rows
	df = pd.read_excel(input_path, nrows=nrows, header=None, sheet_name="HORIZONTAL VIEW")


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



	# 	The year for each date should be made to be the year inputted by the user, or the next year if January has been crossed
	
	df['Date'] = df['Date'].apply(lambda date: custom_datetime_format_convert(date))
	
	if 'year_first' in locals():
		year_to_replace = year_first

	dates_list = []
	for i, v in df.iterrows():
		date = v['Date']
		date = datetime.strptime(date, "%d %B %Y")
		if i >= 1:
			prev_date = df['Date'][i-1]
			prev_date = datetime.strptime(prev_date, "%d %B %Y")
			if date.month == 1 and prev_date.month == 12:
				year_to_replace += 1
		date = date.replace(year=year_to_replace)
		dates_list.append(date)
	
	df['Date'] = dates_list

	# Filter based on date range selected by user
	df = df[df['Date'].apply(lambda x: x >= date_start and x <= date_end)]


	# Making dates and rota_list lists
	dates = []
	for i, v in df['Date'].iteritems():
		v = v.to_pydatetime()
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
		date_string = datetime.strftime(date, '%d/%m/%Y')

		if entry in entries_to_exclude: # If entry is not to be added to output calendar - skip and don't add to entry list
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
	print(convert('../../../user_input/input_brighton_medicine.xlsx', {
		'row_number': '47',
		'date_start': '2019-08-07',
		'date_end': '2019-12-03'
	}))