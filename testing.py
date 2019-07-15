from sched import scheduler
import time
import os

def create_new_folder():
	folder = 'testing_scheduler_folder'
	if not os.path.isdir(folder):
		print('creating new folder')
		os.mkdir(folder)
	else:
		print('folder already exists')

while True:
	s = scheduler()
	s.enter(2, 1, create_new_folder)
	s.run()