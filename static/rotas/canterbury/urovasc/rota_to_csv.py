# Imports
import numpy as np
import pandas as pd
from docx import Document
import os
from datetime import date, timedelta, datetime
import re

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from utilities import *

# Always add when using pandas
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 150)

def ColNum2ColName(n):
   convertString = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
   base = 26
   i = n - 1

   if i < base:
      return convertString[i]
   else:
      return ColNum2ColName(i//base) + convertString[i%base]

def convert(input_path, constants):
# Setup
	# Constants of individual
	week_num_start = int(constants['week_num_start'])
	day_of_week_start = constants['day_of_week_start']
	print(day_of_week_start)
	date_start = datetime.strptime(constants['date_start'], '%Y-%m-%d')
	date_end = datetime.strptime(constants['date_end'], '%Y-%m-%d')
	
	# Constants of rota
	possible_rota_entries = ['Stnd Day', 'Long Day', 'Half Day']
	days_of_week = [
		'Monday',
		'Tuesday',
		'Wednesday',
		'Thursday',
		'Friday',
		'Saturday',
		'Sunday'
	]

# Main
	# Read file
	df = pd.read_excel(input_path, header=None)

	# Match indexes and headers to excel
	df.columns = [ColNum2ColName(i+1) for i, v in enumerate(df.columns)]
	df.index = pd.Series(df.index).shift(-1).fillna(len(df.index)).astype(int)

	# Establish the type of rota variant (either pasted into normal microsoft office (type 1) or libreoffice (type 2))
	if df.shape[0] == 22:
		rota_variant_type = 1
	elif df.shape[0] == 7:
		rota_variant_type = 2

	# Change into a vertical, clean rota
		# Store days of week as rota says
	days_of_week_rota = df.iloc[0].values.tolist()
	days_of_week_rota.remove('WK')
	days_of_week_rota.remove('Name')

	df.columns = df.loc[1].values.tolist()
	df.drop([1], inplace=True)
	if rota_variant_type == 1:
		df.drop([2], inplace=True)
	df.reset_index(inplace=True, drop=True)



	if rota_variant_type == 1:
		# Create numpy array consisting of empty strings, of shape 6, 7, and of dtype object
		dfnp = np.full((6, 7), '', dtype=object)

		dfnp_row_count = 0
		dfnp_col_count = 0
		for df_row_count in range(df.shape[0]):
			if pd.isnull(df.iloc[df_row_count]['Name']):
				if (df_row_count != df.shape[0]-1 and pd.notnull(df.iloc[df_row_count+1]['Name']) ):
					dfnp_row_count += 1
				continue
			for df_col_count in range(2, 9):
				dfnp_col_count = df_col_count-2
				if pd.notnull(df.iloc[df_row_count][df.columns[df_col_count]]):
					dfnp[dfnp_row_count][dfnp_col_count] += df.iloc[df_row_count][df.columns[df_col_count]] + '\n'


		
		# Make df into a DataFrame of the numpy array
		df = pd.DataFrame(dfnp)
	
	df.index = pd.Series(df.index).shift(-1).fillna(len(df.index)).astype(int)
	df.index.name = 'Week'

	df.drop('Name', axis=1, inplace=True) if 'Name' in df.columns else 1
	df.drop('WK', axis=1, inplace=True) if 'WK' in df.columns else 1

	df.columns = days_of_week

	# Setting up dates_dict - a dictionary of lists - to append entries to later
	dates_dict = {}
	dates_dict['start date'] = []
	dates_dict['end date'] = []
	dates_dict['subject'] = []
	dates_dict['all day event'] = []

	date_crawl = date_start
	count = 0
	row_crawl = week_num_start
	col_crawl = df.columns.tolist().index(day_of_week_start)
	
	print(df)
	print(df.shape)

	while date_crawl <= date_end and count < 1000:
		count += 1
		entry = df[df.columns.tolist()[col_crawl]][row_crawl]

		print(col_crawl, row_crawl, date_crawl, entry)
		if pd.isnull(entry) or 'ZERO HOURS' in entry:
			pass
		else:
			for poss in possible_rota_entries:
				if poss in entry:
					subject = poss
					dates_dict['start date'].append(date_crawl.strftime('%d/%m/%Y'))
					dates_dict['end date'].append( (date_crawl+timedelta(days=1)).strftime('%d/%m/%Y') )
					dates_dict['subject'].append(subject)
					dates_dict['all day event'].append('True')

		# Advance col_crawl (and row_crawl if end of column)
		if col_crawl == df.shape[1]-1: # If the crawl is at an end column,
			if row_crawl == df.shape[0]: # If the crawl is also at an end row,
				col_crawl = 0		#...reset crawler to the first column, first row
				row_crawl = 1
			elif row_crawl != df.shape[0]: #Or if the crawl is NOT also at an end row,
				col_crawl = 0
				row_crawl += 1		#...increment to the first column and NEXT row
		else:							# Or if the crawl is not at an end column, just move to the next column, same row
			col_crawl += 1

		# Advance date_crawl
		date_crawl = date_crawl + timedelta(days=1)

	df_result = pd.DataFrame(dates_dict)
	return df_result

if __name__ == '__main__':
	print(os.getcwd())
	print(convert('../../../user_input/input_canterbury_urovasc_type_2.xlsx', {
		'date_start': '2018-04-03',
		'date_end': '2019-06-04',
		'week_num_start': '3',
		'day_of_week_start': 'Wednesday'
	}))
