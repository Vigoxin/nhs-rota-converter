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
	row_start = int(constants['row_start'])
	row_end = int(constants['row_end'])

	# Main
	df = pd.read_excel(input_file_name, header=None)
	df.columns = [chr(65+i) for i, rota_entry in enumerate(df.columns)]
	df.index = pd.Series(df.index).shift(-1).fillna(len(df.index)).astype(int)

	print(df)
	df = df.rename(columns={'B': 'Date'})
	df = df[['Date', col_letter]].loc[row_start:row_end, :]

	# Dropping columns that are null/not a timestamp in the date column
	df = df[pd.notnull(df['Date'])]

	# Making dates and rota_list lists
	dates = []
	for i, v in df['Date'].iteritems():
		if isinstance(v, int):
			v = v.to_pydatetime()
		elif isinstance(v, str):
			v = datetime.strptime(v, '%A, %d %B %Y')
		dates.append(v)
	# dates = df['Date'].values.tolist()
	rota_list = df[col_letter].values.tolist()

	# Setting up dates_dict - a dictionary of lists - to append entries to later
	dates_dict = {}
	dates_dict['start date'] = []
	dates_dict['end date'] = []
	dates_dict['subject'] = []
	dates_dict['all day event'] = []

	for i, rota_entry in enumerate(rota_list):
		print(dates[i], f'({type(dates[i])})', rota_entry, f'({type(rota_entry)})')
		date = dates[i]

		if isinstance(rota_entry, float) and pd.isnull(rota_entry): # If entry is NaN, skip, don't add to entry list
			continue
		elif rota_entry.upper() in ['BH', 'OFF']:
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
	df_result = convert('../../../user_input/input_brighton_paeds.xlsx', {
		'column_letter': 'W',
		'row_start': '139',
		'row_end': '262'
	})
	print(df_result)