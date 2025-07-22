import schedule
import time
from datetime import datetime, timedelta

# infinite function (will it block schedule execution?)
def infinite_call():
  print('infinite_call()')
  while True:
    pass

# print to test if execution is blocked 
def print_call():
  print('print_call()')

# create test times
now = datetime.now()
infinite_time = (now + timedelta(minutes=1)).strftime("%H:%M")
print_time = (now + timedelta(minutes=2)).strftime("%H:%M")

# schedule 1 min, infinite call
schedule.every().day.at(infinite_time).do(
  infinite_call
)
# schedule 2 min, print
schedule.every().day.at(print_time).do(
  print_call
)

while True:
  schedule.run_pending()
  time.sleep(1)