#!/usr/bin/env python
import itertools

# cell email to sms gateways
gateways = {
    'att': 'mms.att.net',
    'boost': 'myboostmobile.com',
    'cricket': 'mms.cricketwireless.net',
    'sprint': 'pm.sprint.com',
    'tmobile': 'tmomail.net',
    'uscc': 'mms.uscc.net',
    'verizon': 'vzwpix.com',
    'virgin': 'vmpix.com'
}

# only care about 512 numbers
first = '512'

with open('second_uniq.txt') as df:
    second_nums = df.readlines()

second = [x.strip() for x in second_nums]

with open('third_uniq.txt') as df:
    third_nums = df.readlines()

third = [x.strip() for x in third_nums]

for s_num in second:
    for t_num in third:
        print(first + s_num + t_num)
