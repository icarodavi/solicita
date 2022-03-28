from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from decouple import config


class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
    bucket_name = config('AWS_STORAGE_BUCKET_NAME')


class StaticStorage(S3Boto3Storage):
    location = settings.AWS_STATIC_LOCATION


class PublicMediaStorage(S3Boto3Storage):
    location = settings.AWS_PUBLIC_MEDIA_LOCATION
    file_overwrite = True
    custom_domain = '{}.s3.amazonaws.com'.format(
        config('AWS_STORAGE_BUCKET_NAME'))


class PrivateMediaStorage(S3Boto3Storage):
    location = settings.AWS_PRIVATE_MEDIA_LOCATION
    default_acl = 'private'
    file_overwrite = True
    custom_domain = False
