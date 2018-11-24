# Imports
import numpy as np
import pandas as pd
import os
from datetime import date, timedelta, datetime

# Always add when using pandas
pd.set_option('display.max_columns', 10)

def convert(input_path, constants):
	
	# Constants
	input_file_name = input_path

	# Constants of individual
	name = constants['name'].title()
	print(name)

	# legend = {
	# 	'DAY': ['08:30', '17:00'],
	# 	'LD': ['08:00', '21:00'],
	# 	'LD-C': ['08:00', '21:00'],
	# 	'NIGHT': ['20:00', '09:00'],
	# 	'EVE': ['13:00', '21:00'],
	# 	'TWIG': ['13:00', '21:00'],
	# }
	
	# Setting up results dictionary
	dates_dict = {}
	dates_dict['subject'] = []
	dates_dict['start date'] = []
	dates_dict['end date'] = []
	dates_dict['all day event'] = []

	# Setting up list of sheet names
	sheet_names = pd.ExcelFile(input_file_name).sheet_names

	# Main
	for sheet in sheet_names:
		print(sheet)
		df = pd.read_excel(input_file_name, sheet_name=sheet, header=None)
		first_col = df[0].tolist()
		for i in range(0, len(first_col)):
			if i not in [0, 1]:
				if not isinstance(first_col[i], str):
					count = i-1
					break
		print(count)
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
			print('df: ', df)
			df.dropna(inplace=True, how='all')
			df = df[pd.notnull(df[name])]
			print('df after dropna: ', df)

			# Bit more cleaning up
			dates = df['Date'].values.tolist()
			rota_list = [str(el).replace(' (swap)', '') for el in df[name].values.tolist()] # ignoring where it says 'swap'
			rota_list = [np.nan if r == ' ' else r for r in rota_list]

			# Get rid of any entries where the date is NaN
			for i in range(len(dates)-1, -1, -1):
				el = dates[i]
				if not isinstance(el, str):
					dates.pop(i)
					rota_list.pop(i)


			for i, el in enumerate(rota_list):
				# print(el)
				date_string = dates[i]
				date = datetime.strptime(date_string, '%d-%b')
				is_weekend = False
				if date.weekday() >= 5:
					is_weekend = True
				days_to_add = 1 if el == 'NIGHT' else 0
				days_to_add = 1

				if (isinstance(el, str) and el not in ['OFF', 'X', 'BH', 'A/L', 'AL']):
						subject = 'Normal' if isinstance(el, float) else el
						dates_dict['subject'].append(subject)
						dates_dict['start date'].append(date.strftime('%d/%m/%Y'))
						dates_dict['end date'].append( (date+timedelta(days=days_to_add)).strftime('%d/%m/%Y') )
						dates_dict['all day event'].append('True')



	# for key in dates_dict:
	# 	print(key, dates_dict[key], len(dates_dict[key]))

	df_result = pd.DataFrame(dates_dict)

	return df_result

if __name__ == '__main__':
	print(convert('../user_input/input.csv', 'Deanne Bell'))