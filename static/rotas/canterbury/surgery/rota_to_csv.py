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
	col_letter = constants['column_letter'].upper()

	# Main
	df = pd.read_csv(input_file_name)

	df.drop(0, inplace=True)
	df.columns = [chr(65+i) for i, el in enumerate(df.columns)]

	dates = df['A'].values.tolist()
	rota_list = df[col_letter].values.tolist()
	rota_list = [np.nan if r == ' ' else r for r in rota_list]

	for i in range(len(dates)-1, -1, -1):
		el = dates[i]
		if not isinstance(el, str):
			dates.pop(i)
			rota_list.pop(i)

	dates_dict = {}
	dates_dict['subject'] = []
	dates_dict['start date'] = []
	dates_dict['end date'] = []
	dates_dict['all day event'] = []

	for i, el in enumerate(rota_list):
		date_string = dates[i]
		date = datetime.strptime(date_string, '%d/%m/%Y')
		is_weekend = False
		if date.weekday() >= 5:
			is_weekend = True

		if (isinstance(el, str) and el != 'Z') or (isinstance(el, float) and np.isnan(el) and not is_weekend):
				subject = 'Normal' if isinstance(el, float) and (np.isnan(el) or el == ' ') else el
				dates_dict['subject'].append(subject)
				dates_dict['start date'].append(date_string)
				dates_dict['end date'].append( (date+timedelta(days=1)).strftime('%d/%m/%Y') )
				dates_dict['all day event'].append('True')

	df_result = pd.DataFrame(dates_dict)

	return df_result

# print(convert('../input/input.xlsx', '../output/output.csv', 'D'))
if __name__ == '__main__':
	print(convert('../user_input/input', 'D'))

# df_result.to_csv('output/' + output_file_name, index=False)
# os.system("open {}".format('output/' + output_file_name))