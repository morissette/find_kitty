## This is a cool hack I did when I lost my cat

I think it's worth sharing because I created a distributed mass email system in one night for the greater good of finding a lost cat.

Now; it is a bit spammy but since it is not commercial, I give it a pass.

### Code synopsis

1. Generate lists: # used to generate permutations of phone number portions

```
for i in `seq 0 999`; do printf "%03d\n" $i; done > second_uniq.txt # second section of a phone number
for i in `seq 0 9999`; do printf "%04d\n" $i; done > third_uniq.txt # third section of a phone number
```

2. Generate all possible numbers # generates possible phone numbers

```
./gen_number_list.py > all_numbers.txt
```

3. Generate all possible cell provider emails # transpose numbers to possible emails

```
./gen_email_list.py > all_email_list.txt
```

4. Populate SQS with all e-mails # throw emails in aws sqs for processing

```
./populate_sqs.py
```

5. Mass text everyone in a area code via a distributed worker system

**in the following script I set this up to run via digital ocean nodes that were spun up; processed x amount of outbound messages and then spun down the worker node.**

```
./process_emails.py
```

### Yes it's awesome

#### No, I didn't ever find my cat

##### My wife believes our neighbor stole her, because she was a gorgeous calico cat

*No, not happy about it*

