"""
Generate possible emails from phone number
list
Run: ./gen_email_list.py > all_email_list.txt
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
