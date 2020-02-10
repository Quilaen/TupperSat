def log(thing):
	from datetime import datetime as dt
	import time
	import logging
	LOG_DIR = '/home/pi/logs/'
	filename = "Test_Log.txt"
	logging.basicConfig(filename=filename, level = logging.INFO, format = '%(asctime)s %(levelname)s: %(message)s')
	time.sleep(3)
	logging.info(thing)

