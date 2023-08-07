import uuid

import boto3
from django.conf import settings


def create_random_filename(filename):
    extension = filename.split('.')[-1]
    return str(uuid.uuid4()) + '.' + extension


def create_presigned_url(filename):
    client = boto3.client('s3')
    return client.generate_presigned_post(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=filename,
        ExpiresIn=300,
    )
