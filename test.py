import datetime
import time

# Assuming script_start_time and script_end_time are datetime objects
script_start_time = datetime.datetime.now()
calc_start_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

n = 5
for i in range(1, 500000):
    n += 1
time.sleep(2)

script_end_time = datetime.datetime.now()
calc_end_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

equals = '=' * 23
print(equals)

# Calculate duration
duration = script_end_time - script_start_time

# Extract days, hours, minutes, and seconds from the duration
days = duration.days
hours, remainder = divmod(duration.seconds, 3600)
minutes, seconds = divmod(remainder, 60)

duration_for_test = duration.total_seconds()

test = 500 / duration_for_test / 60
print(test)

print(f"Duration: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds")