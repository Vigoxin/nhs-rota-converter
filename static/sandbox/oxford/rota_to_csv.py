# Imports
import numpy as np
import pandas as pd
import os
from datetime import date, timedelta, datetime

# Always add when using pandas
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 100)

def convert(input_path, constants):

	# Constants
	input_file_name = input_path

	# Constants of individual
	col_letter = constants['column_letter'].upper()
	row_start = constants['row_start']
	row_end = constants['row_end']

	# Main
	df = pd.read_excel(input_file_name, header=None)
	df.columns = [chr(65+i) for i, el in enumerate(df.columns)]
	df.index = pd.Series(df.index).shift(-1).fillna(0).astype(int)

	df = df.rename(columns={'A': 'Date'})
	df = df[['Date', col_letter]].loc[row_start:row_end, :]

	# Dropping columns that are null/not a timestamp in the date column
	df = df[pd.notnull(df['Date'])]

	# Making dates and rota_list lists
	dates = []
	for i, v in df['Date'].iteritems():
		v = v.to_pydatetime()
		dates.append(v)
	rota_list = df[col_letter].values.tolist()

	# Setting up dates_dict - a dictionary of lists - to append entries to later
	dates_dict = {}
	dates_dict['start date'] = []
	dates_dict['end date'] = []
	dates_dict['subject'] = []
	dates_dict['all day event'] = []

	for i, el in enumerate(rota_list):
		date = dates[i]
		date_string = datetime.strftime(date, '%d/%m/%Y')

		if isinstance(el, float) and pd.isnull(el): # If entry is NaN, skip, don't add to entry list
			continue				
		else:						# If entry is not NaN
			subject = el			# then make the subject whatever it says and add it to the final list
		dates_dict['start date'].append(date_string)
		dates_dict['end date'].append( (date+timedelta(days=1)).strftime('%d/%m/%Y') )
		dates_dict['subject'].append(subject)
		dates_dict['all day event'].append('True')

	df_result = pd.DataFrame(dates_dict)
	return df_result

if __name__ == '__main__':
	df_result = convert('input/input.xlsx', {
		'column_letter': 'M',
		'row_start': 104,
		'row_end': 196
	})
	print(df_result)