from datetime import datetime, timedelta
from urllib.parse import parse_qsl, urlencode, urlsplit

import boto3
from botocore.config import Config
from decouple import config
from django.conf import settings
from django.utils.encoding import filepath_to_uri
from storages.backends.s3boto3 import S3Boto3Storage
from utils.s3urls import create_presigned_url


class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
    bucket_name = config('AWS_STORAGE_BUCKET_NAME')


class StaticStorage(S3Boto3Storage):
    location = settings.AWS_STATIC_LOCATION
    custom_domain = '{}.s3.amazonaws.com'.format(
        config('AWS_STORAGE_BUCKET_NAME'))

    def url(self, name, parameters=None, expire=None, http_method=None):
        # Preserve the trailing slash after normalizing the path.
        name = self._normalize_name(self._clean_name(name))
        params = parameters.copy() if parameters else {}
        if expire is None:
            expire = 3600

        if self.custom_domain:
            url = '{}//{}/{}{}'.format(
                'http:',
                self.custom_domain,
                filepath_to_uri(name),
                '?{}'.format(urlencode(params)) if params else '',
            )

            # if self.querystring_auth and self.cloudfront_signer:
            #     expiration = datetime.utcnow() + timedelta(seconds=36000)
            #     return self.cloudfront_signer.generate_presigned_url(url, date_less_than=expiration)

            # return url
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
        # try:
        #     response = s3_client.generate_presigned_url('get_object',
        #                                                 Params={'Bucket': bucket_name,
        #                                                         'Key': object_name},
        #                                                 ExpiresIn=expiration)
        # except ClientError as error:
        #     logging.error(error)
        #     return None
        params['Bucket'] = config('AWS_STORAGE_BUCKET_NAME')
        params['Key'] = name
        url = s3_client.generate_presigned_url('get_object', Params=params,
                                               ExpiresIn=expire, HttpMethod=http_method)
        if settings.AWS_QUERYSTRING_AUTH:
            return url
        # return self._strip_signing_parameters(url)
        return create_presigned_url('solicitacao', 'static/'+name)

    def _strip_signing_parameters(self, url):

        split_url = urlsplit(url)
        qs = parse_qsl(split_url.query, keep_blank_values=True)
        blacklist = {
            'x-amz-algorithm', 'x-amz-credential', 'x-amz-date',
            'x-amz-expires', 'x-amz-signedheaders', 'x-amz-signature',
            'x-amz-security-token', 'awsaccesskeyid', 'expires', 'signature',
        }
        filtered_qs = ((key, val)
                       for key, val in qs if key.lower() not in blacklist)
        # Note: Parameters that did not have a value in the original query string will have
        # an '=' sign appended to it, e.g ?foo&bar becomes ?foo=&bar=
        joined_qs = ('='.join(keyval) for keyval in filtered_qs)
        split_url = split_url._replace(query='&'.join(joined_qs))
        return split_url.geturl()


class PublicMediaStorage(S3Boto3Storage):
    location = settings.AWS_PUBLIC_MEDIA_LOCATION
    file_overwrite = True
    # custom_domain = '{}.s3.amazonaws.com'.format(config('AWS_STORAGE_BUCKET_NAME'))
    # custom_domain = '{}.s3.amazonaws.com'.format(config('AWS_STORAGE_BUCKET_NAME'))

    def url(self, name, parameters=None, expire=None, http_method=None):
        return create_presigned_url(config('AWS_STORAGE_BUCKET_NAME'), 'media/public/'+name)


class PrivateMediaStorage(S3Boto3Storage):
    location = settings.AWS_PRIVATE_MEDIA_LOCATION
    default_acl = 'private'
    file_overwrite = True
    custom_domain = False

    def url(self, name, parameters=None, expire=None, http_method=None):
        return create_presigned_url(config('AWS_STORAGE_BUCKET_NAME'), 'media/private/'+name)
