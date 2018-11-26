# Imports
import numpy as np
import pandas as pd
import os
from datetime import date, timedelta, datetime

# Always add when using pandas
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 150)

def convert(input_path, constants):

	# Constants
	input_file_name = input_path

	# Constants of individual
	col_letter = constants['column_letter'].upper()

	# Main
	df = pd.read_excel(input_file_name, header=None)
	df.columns = [chr(65+i) for i, el in enumerate(df.columns)]
	
	df = df[['A', col_letter]]
	df.columns = ['Date', col_letter]
	df['type'] = df.apply(lambda x: type(x['Date']), axis=1)
	df.drop([0, 1], inplace=True)
	print(df)

	dates = df['Date'].values.tolist()
	rota_list = df[col_letter].values.tolist()

	# Clip ending values of dates and rota_list so that the last value is the last date, NOT a NaN and the total on call days as in the spreadsheet
	for i in range(len(dates)-1, -1, -1):
		el = dates[i]
		if isinstance(el, float) and np.isnan(el):
			dates.pop(i)
			rota_list.pop(i)

	# Setting up dates_dict - a dictionary of lists - to append entries to later
	dates_dict = {}
	dates_dict['subject'] = []
	dates_dict['start date'] = []
	dates_dict['end date'] = []
	dates_dict['all day event'] = []

	for i, el in enumerate(rota_list):
		date = dates[i]
		date_string = datetime.strftime(date, '%d/%m/%Y')
		
		is_weekend = False if date.weekday() < 5 else True

		if el != 'Z': 					#If it's not already a zero day
			if isinstance(el, float) and pd.isnull(el): # If entry is NaN
				if is_weekend:			#If it's a weekend, then don't add to the entry final list
					continue
				elif not is_weekend:	#If it's a weekday, make the subject 'normal hours' and add to the final list
					subject = 'Normal hours'
			else:						# If entry is not NaN
				subject = el			# then make the subject whatever it says and add it to the final list
			
			dates_dict['subject'].append(subject)
			dates_dict['start date'].append(date_string)
			dates_dict['end date'].append( (date+timedelta(days=1)).strftime('%d/%m/%Y') )
			dates_dict['all day event'].append('True')

	df_result = pd.DataFrame(dates_dict)
	return df_result

if __name__ == '__main__':
	df_result = convert('../../../user_input/input_ashford.xlsx', {'column_letter': 'C'})
	# print(df_result)