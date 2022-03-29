
# from django.conf import settings
from decouple import config
from botocore.exceptions import ClientError
from botocore.config import Config
import boto3
import logging


def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    s3_signature = {
        'v4': 's3v4',
        'v2': 's3'
    }
    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3', aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
                             aws_secret_access_key=config(
                                 'AWS_SECRET_ACCESS_KEY'),
                             region_name=config('AWS_DEFAULT_REGION'),
                             config=Config(signature_version=s3_signature['v4']))
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as error:
        logging.error(error)
        return None

    # The response contains the presigned URL
    return response


if __name__ == '__main__':
    url = create_presigned_url('solicitacao', 'static/favicon.ico')
    print(url)
