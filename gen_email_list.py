"""
Generate possible emails from phone number
list
"""

with open('all_numbers.txt') as df:
    numbers = df.readlines()

# strip newlines
numbers = [x.strip() for x in numbers]

# gen popular emails for carriers
for number in numbers:
    number = str(number)
    print(number + '@txt.att.net')
    print(number + '@vtext.com')
    print(number + '@messaging.sprintpcs.com')
    print(number + '@tmomail.net')
