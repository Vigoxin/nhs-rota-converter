# Imports
import numpy as np
import pandas as pd
import os
from datetime import date, timedelta, datetime

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from utilities import *

# Always add when using pandas
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 100)
pd.set_option('display.width', 120)

def convert(input_path, constants):

# Setup
	# Constants of individual

	# Constants of rota format
	dates_letnum = 'A' #the column/row which has the dates in it
	rota_datetime_format = '%d-%b'
	entries_to_exclude = ['Zero Hours', 'Leave', np.nan]

# Main
	# Read file
	sheet_names = pd.ExcelFile(input_path).sheet_names
	df = pd.read_excel(input_path,header=None)

	# Match indexes and headers to excel
	df.columns = [ColNum2ColName(i+1) for i, v in enumerate(df.columns)]
	df.index = pd.Series(df.index).shift(-1).fillna(len(df.index)).astype(int)

	# Get rid of columns which consist of only NaN values
	df.dropna(how='all', axis=1, inplace=True)

	# Keep only rows which have a datetime in the date column (will use date_column_index later)
	date_column_index = pd.Index(df.isin(["Monday Date"]).any(axis="rows")).get_loc(True)
	date_column = df.columns[date_column_index]
	df = df[df[date_column].apply(lambda x: isinstance(x,datetime))]

	
	# Setting up dates_dict - a dictionary of lists - to append entries to later
	dates_dict = {}
	dates_dict['subject'] = []
	dates_dict['start date'] = []
	dates_dict['end date'] = []
	dates_dict['all day event'] = []

	for row, v in df[date_column].iteritems():
		monday_date = v
		
		for i in range(7):
			date = monday_date + timedelta(days=i)
			
			i += 1
			col = df.columns[date_column_index+i]
			rota_entry = df[col][row]

			if rota_entry not in entries_to_exclude:
				subject = rota_entry.replace("\n", " - ")
				dates_dict['start date'].append(date.strftime('%d/%m/%Y'))
				dates_dict['end date'].append( (date+timedelta(days=1)).strftime('%d/%m/%Y') )
				dates_dict['subject'].append(subject)
				dates_dict['all day event'].append('True')

			date = date + timedelta(days=1)


	df_result = pd.DataFrame(dates_dict)
	return df_result

if __name__ == '__main__':
	df_result = convert('../../../user_input/input_winchester_medicine.xlsx', {
	})
	print(df_result)