# Setup
	# Constants of individual
	col_letter = constants['column_letter'].upper()

	# Constants of rota format
	rota_datetime_format = '%d/%m/%y'
	dates_letnum = 'A' #the column/row which has the dates in it
	entries_to_exclude = ['Z']

# Main
	# Read file

	# Match indexes and headers to excel

	# Define number of rows to read: If rota is horizontal, then specify nrows for pd.read_excel. If rota is vertical, then nrows=None

	# Load again but only nrows number of rows

	# Match indexes and headers to excel

	# Drop hidden rows

	# Change into a vertical rota with dates as rows and columns as 'dates' and 'person'

	# Rename 'Date' column

	# Filter columns (only dates column and person's rota entries column should remain at the end)

	# Filter rows (only include rows with entries to be included)

	# Making dates and rota_list lists

	# Setting up dates_dict - a dictionary of lists - to append entries to later
