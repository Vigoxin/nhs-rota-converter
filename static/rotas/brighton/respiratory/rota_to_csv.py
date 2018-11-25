# Imports
import numpy as np
import pandas as pd
import os
import re
from datetime import date, timedelta, datetime

# Always add when using pandas
pd.set_option('display.max_columns', 10)

def convert(input_path, constants):
	
	# Constants
	input_file_name = input_path

	# Constants of individual
	name = constants['name']
	print(name)
	year_first = int(constants['year_first'])
	print(year_first)
	
	# Setting up results dictionary of lists
	dates_dict = {}
	dates_dict['subject'] = []
	dates_dict['start date'] = []
	dates_dict['end date'] = []
	dates_dict['all day event'] = []

	# Setting up list of sheet names
	sheet_names = pd.ExcelFile(input_file_name).sheet_names

	# Main
	year_first_switch_count = 0
	for sheet in sheet_names:
		df = pd.read_excel(input_file_name, sheet_name=sheet, header=None)
		first_col = df[0].tolist()
		for i in range(0, len(first_col)):
			if i not in [0, 1]:
				if not isinstance(first_col[i], str):
					count = i-1
					break
		# print(count)
		# ^ calculating number of rows to read again

		df = pd.read_excel(input_file_name, sheet_name=sheet, nrows=count, header=None)

		# Manipulating to make easy to convert into lists
		df = pd.DataFrame.transpose(df)
		df.columns = df.iloc[0]
		if name in df.columns.tolist():
			df_col_temp = df.columns.tolist().copy()
			df_col_temp[0] = 'Date'
			df_col_temp[1] = 'Day'
			df.columns = df_col_temp
			df = df[['Date', 'Day', name]]
			df.drop([0, 1], inplace=True)
			# print('df: ', df)
			df.dropna(inplace=True, how='all')
			df = df[pd.notnull(df[name])]
			# print('df after dropna: ', df)

			# Bit more cleaning up
			dates = df['Date'].values.tolist()
			rota_list = [str(el).replace(' (swap)', '') for el in df[name].values.tolist()] # ignoring where it says 'swap'
			rota_list = [np.nan if r == ' ' else r for r in rota_list]
			# print(rota_list)

			# # Get rid of any entries where the date is NaN
			# print(len(dates))
			# for i in range(len(dates)-1, -1, -1):
			# 	date_string = dates[i]
			# 	if not (isinstance(date_string, datetime) or isinstance(date_string, str)):
			# 		dates.pop(i)
			# 		rota_list.pop(i)
			# print(len(dates))

			for i, rota_entry in enumerate(rota_list):
				if isinstance(dates[i], str):
					date_string = dates[i]
					date = datetime.strptime(date_string, '%d-%b')
				elif isinstance(dates[i], datetime):
					date = dates[i]
					
				# If anywhere from the second date onwards the month is January, and it hasn't been done before already, then year_first should be increased by one. This is to accommodate rotas crossing December into January
				if (sheet_names.index(sheet) == 0 and i >= 1) or (sheet_names.index(sheet) >=1):
					if date.month == 1 and year_first_switch_count == 0:
						year_first += 1
						year_first_switch_count += 1

				# The year should be made to be the year inputted by the user, or the next year if January has been crossed
				date = date.replace(year=year_first)

				is_weekend = False
				if date.weekday() >= 5:
					is_weekend = True
				days_to_add = 1 if rota_entry == 'NIGHT' else 0
				days_to_add = 1

				if (isinstance(rota_entry, str) and rota_entry not in ['OFF', 'X', 'BH', 'A/L', 'AL']):
						subject = rota_entry
						dates_dict['subject'].append(subject)
						dates_dict['start date'].append(date.strftime(f'%d/%m/%Y'))
						dates_dict['end date'].append( (date+timedelta(days=days_to_add)).strftime('%d/%m/%Y') )
						dates_dict['all day event'].append('True')



	# for key in dates_dict:
	# 	print(key, dates_dict[key], len(dates_dict[key]))

	df_result = pd.DataFrame(dates_dict)

	return df_result

if __name__ == '__main__':
	print(os.getcwd())
	print(convert('../../../user_input/input_brighton_resp.xlsx', {'name': 'Shruti Dorai', 'year_first': '2018'}))