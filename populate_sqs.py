"""
Upload emails to SQS
"""
import os
import uuid

from boto3.session import Session

def setup_client():
    """
    Setup AWS Session and SQS
    client
    :return client: SQS client
    """
    session = Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
        region_name=os.getenv("AWS_REGION")
    )
    client = session.client('sqs')
    return client

def add_to_sqs(client, emails):
    """
    Add item to queue in batch
    :param client: Session
    :param emails: List of emails to add
    """
    entries = []

    # build body for aws api
    # http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.Client.send_message_batch
    for email in emails:
        unique_id = str(uuid.uuid4())
        entries.append({
            'Id': unique_id,
            'MessageBody': email
        })

    # send request
    response = client.send_message_batch(
        QueueUrl='https://sqs.us-west-1.amazonaws.com/117905818048/Emails',
        Entries=entries
    )
    if response.get('Successful', None) is not None:
        return emails
    return None


def run():
    client = setup_client()

    # load emails
    with open('all_email_list.txt') as df:
        emails = df.read().splitlines()
        process_emails(client, emails)


def process_emails(client, emails):
    """
    process emails into sqs
    :param client:
    :param emails:
    """
    iteration = 0

    # setup tmp vars for batch uploading
    counter = 0
    list_to_send = []

    # hold for retry requests
    retries = []

    # get sets of 10 emails to send to sqs
    for email in emails:
        if iteration < 145930:
            print(iteration)
            iteration += 1
            continue

        if counter == 10:

            # setup retries for failed import sets
            retry = add_to_sqs(client, list_to_send)
            if retry is not None:
                retries.append(retry)

            # reset tmp vars
            counter = 0
            list_to_send = []

            iteration += 1
            print(iteration)

        # add email to list
        list_to_send.append(email)

        # increment
        counter += 1

    process_failed_requests(client, retries)


def process_failed_requests(client, retries):
    """
    retry any failed batch uploads to SQS
    :param client:
    :param retry:
    """
    for retry in retries:
        retry = add_to_sqs(client, retry)
        if retry is not None:
            print('unable to add the following batch: %s' % retry)

if __name__ == '__main__':
    run()
