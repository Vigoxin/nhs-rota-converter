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
	sheet_num = int(constants['sheet_num'])-1
	row_number = int(constants['row_number'])

	# Constants of rota format
	dates_letnum = 'A' #the column/row which has the dates in it
	rota_datetime_format = '%d-%b'
	entries_to_exclude = ['Zero', np.nan]

# Main
	# Read file
	sheet_names = pd.ExcelFile(input_path).sheet_names
	df = pd.read_excel(input_path, sheet_name=sheet_names[sheet_num],header=None)

	# Match indexes and headers to excel
	df.columns = [ColNum2ColName(i+1) for i, v in enumerate(df.columns)]
	df.index = pd.Series(df.index).shift(-1).fillna(len(df.index)).astype(int)

	# Get rid of columns which consist of only NaN values
	df.dropna(how='all', axis=1, inplace=True)

# Splits multiple tables from the same dataframe into separate ones, as separated by at least one row of all NaNs
	dfs = split_df(df)

	# Create a micro and macro rota df
	df_micro = dfs[2]
	df_macro = dfs[3]

	# Create a list of two dfs representing the macro rota - one where the first row of dates is used, and then one where the second row of dates is used
	df_macro.drop(df_macro.index[0], inplace=True)
	
	df_macros = []
	df_macros.append(df_macro.copy(deep=True))
	df_macros.append(df_macro.copy(deep=True))
	
	for i in range(2):
		df_macros[i].index = ['Date' if el == df_macros[i].index[i] else el for el in df_macros[i].index.tolist()]
		df_macros[i] = df_macros[i].T[['Date', row_number]]
		df_macros[i].drop(df_macros[i].index[[0,1]], inplace=True)

	# Make one df_macro which concats the two to have all the dates in chronological order
	df_macro = pd.concat([df_macros[0], df_macros[1]])
	df_macro.reset_index(drop=True, inplace=True)
	df_macro = df_macro[df_macro['Date'].notnull()]
	
	# Clean up df_micro
	df_micro.columns = df_micro.iloc[0]
	df_micro.drop(df_micro.index[0], inplace=True)
	
	# Setting up dates_dict - a dictionary of lists - to append entries to later
	dates_dict = {}
	dates_dict['subject'] = []
	dates_dict['start date'] = []
	dates_dict['end date'] = []
	dates_dict['all day event'] = []

	for ma, v in df_macro['Date'].iteritems():
		date = df_macro['Date'][ma]
		rota_week_num = df_macro[row_number][ma]
		
		for i in range(7):
			i += 2
			week = df_micro[df_micro['Week'] == rota_week_num].iloc[0]
			ward = week['Duty']
			rota_entry = week[i]

			if rota_entry not in entries_to_exclude:
				subject = f'{rota_entry} - {ward}'			
				dates_dict['start date'].append(date.strftime('%d/%m/%Y'))
				dates_dict['end date'].append( (date+timedelta(days=1)).strftime('%d/%m/%Y') )
				dates_dict['subject'].append(subject)
				dates_dict['all day event'].append('True')

			date = date + timedelta(days=1)

	df_result = pd.DataFrame(dates_dict)
	return df_result

if __name__ == '__main__':
	df_result = convert('../../../user_input/waiting_input_frimley_surgery.xlsx', {
		'sheet_num': '3',
		'row_number': '33'
	})
	print(df_result)