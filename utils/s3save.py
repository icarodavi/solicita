import logging
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
from decouple import config
import os


def up_file(file, obj=None):
    if obj is None:
        obj = os.path.basename(file)
    s3_signature = {
        'v4': 's3v4',
        'v2': 's3'
    }
    s3_client: boto3.client = boto3.client('s3', aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
                                           aws_secret_access_key=config(
        'AWS_SECRET_ACCESS_KEY'),
        region_name=config('AWS_DEFAULT_REGION'),
        config=Config(signature_version=s3_signature['v4']))
    try:
        response = s3_client.upload_file(
            file, config('AWS_STORAGE_BUCKET_NAME'), obj)
    except ClientError as e:
        logging.error(e)
        return False
    return True
