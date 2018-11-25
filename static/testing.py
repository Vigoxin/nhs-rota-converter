import re
date_string = "2018-01-04 00:00:00"
print(date_string)

m = re.match('\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', date_string)
print(m)