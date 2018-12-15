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
	date_start = datetime.strptime(constants['date_start'], '%Y-%m-%d')
	date_end = datetime.strptime(constants['date_end'], '%Y-%m-%d')
	
	# Constants of rota
	possible_rota_entries = ['Stnd Day', 'Long Day', 'Half Day']
	# days_of_week_rota_dict = {
	# 	'Monday': 'MON',
	# 	'Tuesday': 'TUES',
	# 	'Wednesday': 'WED',
	# 	'Thursday': 'THURS',
	# 	'Friday': 'FRI',
	# 	'Saturday': 'SAT',
	# 	'Sunday': 'SUN'
	# }

# Main
	# Read file
	df = pd.read_excel(input_path, header=None)

	# Match indexes and headers to excel
	df.columns = [ColNum2ColName(i+1) for i, v in enumerate(df.columns)]
	df.index = pd.Series(df.index).shift(-1).fillna(len(df.index)).astype(int)

	# Change into a vertical, clean rota
		# Store days of week as rota says
	days_of_week_rota = df.iloc[0].values.tolist()
	days_of_week_rota.remove('WK')
	days_of_week_rota.remove('Name')

	df.columns = df.loc[1].values.tolist()
	df.drop([1, 2], inplace=True)
	df.reset_index(inplace=True, drop=True)
		# continue

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

	# Set indexes and columns
	df.columns = days_of_week_rota
	df.index = pd.Series(df.index).shift(-1).fillna(len(df.index)).astype(int)
	df.index.name = 'Week'

	
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
	
	while date_crawl <= date_end and count < 1000:
		count += 1
		entry = df[df.columns.tolist()[col_crawl]][row_crawl]

		# raise
		if pd.isnull(entry) or 'ZERO HOURS' in entry:
			if col_crawl == df.shape[1]-1:
				col_crawl = 0
				row_crawl += 1
			else:
				col_crawl += 1
			if row_crawl == df.shape[0]:
				row_crawl = 1
			date_crawl = date_crawl + timedelta(days=1)
			continue
		else:
			for poss in possible_rota_entries:
				if poss in entry:
					subject = poss
					dates_dict['start date'].append(date_crawl.strftime('%d/%m/%Y'))
					dates_dict['end date'].append( (date_crawl+timedelta(days=1)).strftime('%d/%m/%Y') )
					dates_dict['subject'].append(subject)
					dates_dict['all day event'].append('True')

		if col_crawl == df.shape[1]-1:
			col_crawl = 0
			row_crawl += 1
		else:
			col_crawl += 1
		if row_crawl == df.shape[0]:
			row_crawl = 1
		
		date_crawl = date_crawl + timedelta(days=1)

	df_result = pd.DataFrame(dates_dict)
	return df_result

if __name__ == '__main__':
	print(os.getcwd())
	print(convert('../../../user_input/Book6.xlsx', {
		'date_start': '2018-12-05',
		'date_end': '2019-04-02',
		'week_num_start': '4',
		'day_of_week_start': 'Wednesday'
	}))

