"""
Read file into texts and calls.
It's ok if you don't understand how to read files
"""
import csv
from collections import defaultdict
with open('texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)

"""
TASK 2: Which telephone number spent the longest time on the phone
during the period? Don't forget that time spent answering a call is
also time spent on the phone.
Print a message:
"<telephone number> spent the longest time, <total time> seconds, on the phone during 
September 2016.".
"""

records = defaultdict(int)
for call in calls:
    duration = int(call[-1])
    records[call[0]] += duration
    records[call[1]] += duration
max_duration = 0
max_number = None
for key, value in records.items():
    if value > max_duration:
        max_duration = value
        max_number = key
print(f"{max_number} spent the longest time, {max_duration} seconds, on the phone during September 2016.")
