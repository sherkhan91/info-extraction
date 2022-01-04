import schedule
from . import diffbot_extraction
import time


def start_scheduler():
	print("schedular has been triggered.")

	schedule.every(5).minutes.do(diffbot_extraction.getinformation)
	while True:
		schedule.run_pending()
		time.sleep(1)
