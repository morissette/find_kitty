"""
To prevent blacklist issues with blasting mail
from a single source; adopt a distributed worker
model to process emails across a series of
worker nodes

Note: Digital Ocean uber cheap to do this
"""
import os
import time

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

def query_sqs(client):
    """
    Poll SQS for new messages
    """
    messages = client.receive_message(
        QueueUrl='https://sqs.us-west-1.amazonaws.com/117905818048/Emails',
        AttributeNames=['All'],
        MaxNumberOfMessages=1,
        VisibilityTimeout=500,
        WaitTimeSeconds=20
    )

    if messages.get('Messages'):
        message = messages.get('Messages')[0]
        body = message['Body']
        receipt = message['ReceiptHandle']
        delete_msg(client, receipt)

def delete_msg(client, receipt_handle):
    """
    Delete message from SQS
    """
    response = client.delete_message(
        QueueUrl='https://sqs.us-west-1.amazonaws.com/117905818048/Emails',
        ReceiptHandle=receipt_handle
    )

def send_mail(group):
    subject = '"ALERT! Missing cat in Round Rock, TX"'
    body = '"Have you seen me? https://goo.gl/z1kPWC"'

    command = 'echo ' + body + ' | mail -s ' + subject + ' ' + ' '.join(group)
    return os.system(command)

if __name__ == '__main__':
    client = setup_client()

    while True:
        query_sqs(client)
        time.sleep(5)
