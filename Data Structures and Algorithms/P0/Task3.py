"""
Read file into texts and calls.
It's ok if you don't understand how to read files.
"""
import csv

with open('texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)

"""
TASK 3:
(080) is the area code for fixed line telephones in Bangalore.
Fixed line numbers include parentheses, so Bangalore numbers
have the form (080)xxxxxxx.)

Part A: Find all of the area codes and mobile prefixes called by people
in Bangalore. In other words, the calls were initiated by "(080)" area code
to the following area codes and mobile prefixes:
 - Fixed lines start with an area code enclosed in brackets. The area
   codes vary in length but always begin with 0.
 - Mobile numbers have no parentheses, but have a space in the middle
   of the number to help readability. The prefix of a mobile number
   is its first four digits, and they always start with 7, 8 or 9.
 - Telemarketers' numbers have no parentheses or space, but they start
   with the area code 140.

Print the answer as part of a message:
"The numbers called by people in Bangalore have codes:"
 <list of codes>
The list of codes should be print out one per line in lexicographic order with no duplicates.

Part B: What percentage of calls from fixed lines in Bangalore are made
to fixed lines also in Bangalore? In other words, of all the calls made
from a number starting with "(080)", what percentage of these calls
were made to a number also starting with "(080)"?

Print the answer as a part of a message::
"<percentage> percent of calls from fixed lines in Bangalore are calls
to other fixed lines in Bangalore."
The percentage should have 2 decimal digits
"""
codes = set()
Bangalore_code = "(080)"
Mobile_numbers_code = "789"
Telemarketers_code = "140"
telemarketer_not_found = True
number_of_calls = 0
Bangalore_calls = 0
for call in calls:
    if call[0][:5] == Bangalore_code:
        number_of_calls += 1
        receiver = call[1]
        if receiver[0] == '(':
            code_last_index = receiver.index(')')
            receiver_code = receiver[:code_last_index + 1]
            if receiver_code == Bangalore_code:
                Bangalore_calls += 1
            codes.add(receiver_code)
        elif receiver[0] in Mobile_numbers_code:
            codes.add(receiver[:4])
        elif receiver[:3] == Telemarketers_code and telemarketer_not_found:
            codes.add(Telemarketers_code)
            telemarketer_not_found = False
codes = sorted(codes)
print("The numbers called by people in Bangalore have codes:")
for code in codes:
    print(code)
print(
    f"{round((Bangalore_calls / number_of_calls) * 100, 2)} percent of calls from fixed lines in Bangalore are"
    f" calls to other fixed lines in Bangalore.")
