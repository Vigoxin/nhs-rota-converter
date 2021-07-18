import os
import xlrd
import openpyxl
import pandas as pd
import numpy as np

def find_hidden_row_indexes(input_path):
	hidden_row_indexes = []

	# # Hidden rows if .xls file:
	# if ext == '.xls':
	# 	book = xlrd.open_workbook(input_path, formatting_info=1) #open our xls file, there's lots of extra default options in this call, for logging etc. take a look at the docs
	# 	sheet = book.sheet_by_index(0) #or by the index it has in excel's sheet collection
		
	# 	for r in range(sheet.nrows):
	# 		if sheet.rowinfo_map[r].hidden == 1:
	# 			hidden_row_indexes.append(r+1)

	# Hidden rows if .xlsx file:
	# if ext == '.xlsx':
	if True:
		wb = openpyxl.load_workbook(input_path)
		ws = wb.worksheets[0]

		for rowLetter,rowDimension in ws.row_dimensions.items():
		    if rowDimension.hidden == True:
		        hidden_row_indexes.append(rowLetter)

	return hidden_row_indexes


def ColNum2ColName(n):
   convertString = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
   base = 26
   i = n - 1

   if i < base:
      return convertString[i]
   else:
      return ColNum2ColName(i//base) + convertString[i%base]

# Splits multiple tables from the same Pandas dataframe into separate ones, as separated by at least one row of all NaNs
# df should be the input dataframe. dfs is the output - a list of dataframes.
def split_df(df):
	row_indexes_of_dfs = []
	temp_index_start = 0
	for i in range(df.shape[0]):
		if i >=1:
			# if this is a new full row, store i in the var temp_index_start
			if not df.iloc[i].isnull().all() and df.iloc[i-1].isnull().all():
				temp_index_start = i
			# if this is a new completely empty row, store i in the var temp_index_stop and also add start and stop to row_indexes_of_dfs
			if df.iloc[i].isnull().all() and not df.iloc[i-1].isnull().all():
				temp_index_stop = i
				row_indexes_of_dfs.append({'start': temp_index_start, 'stop': temp_index_stop})
		# if i is last value
		if i == df.shape[0]-1:
				temp_index_stop = i
				row_indexes_of_dfs.append({'start': temp_index_start, 'stop': temp_index_stop})

	dfs = []
	for index_pair in row_indexes_of_dfs:
		df_temp = pd.DataFrame(df.iloc[index_pair['start']:index_pair['stop']])
		dfs.append(df_temp)

	return dfs