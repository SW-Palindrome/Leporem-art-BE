import boto3
from botocore.exceptions import ClientError


def send_email(sender: str, recipient: str, subject: str, html: str):
    client = boto3.client('ses', region_name='ap-northeast-2')
    try:
        response = client.send_email(
            Source=sender,
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Subject': {
                    'Data': subject,
                },
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': html,
                    },
                },
            },
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print(f'Email sent! Message ID: {response["MessageId"]}'),
