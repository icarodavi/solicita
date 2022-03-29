from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from decouple import config
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
        # name = self._normalize_name(self._clean_name(name))
        # params = parameters.copy() if parameters else {}
        # if expire is None:
        #     expire = self.querystring_expire

        # if self.custom_domain:
        #     url = '{}//{}/{}{}'.format(
        #         'http:',
        #         self.custom_domain,
        #         filepath_to_uri(name),
        #         '?{}'.format(urlencode(params)) if params else '',
        #     )

        #     if self.querystring_auth and self.cloudfront_signer:
        #         expiration = datetime.utcnow() + timedelta(seconds=expire)
        #         return self.cloudfront_signer.generate_presigned_url(url, date_less_than=expiration)

        #     return url

        # params['Bucket'] = self.bucket.name
        # params['Key'] = name
        # url = self.bucket.meta.client.generate_presigned_url('get_object', Params=params,
        #                                                      ExpiresIn=expire, HttpMethod=http_method)
        # if self.querystring_auth:
        #     return url
        # return self._strip_signing_parameters(url)
        return create_presigned_url('solicitacao', 'static/'+name)


class PublicMediaStorage(S3Boto3Storage):
    location = settings.AWS_PUBLIC_MEDIA_LOCATION
    file_overwrite = True
    # custom_domain = '{}.s3.amazonaws.com'.format(config('AWS_STORAGE_BUCKET_NAME'))
    # custom_domain = '{}.s3.amazonaws.com'.format(config('AWS_STORAGE_BUCKET_NAME'))


class PrivateMediaStorage(S3Boto3Storage):
    location = settings.AWS_PRIVATE_MEDIA_LOCATION
    default_acl = 'private'
    file_overwrite = True
    custom_domain = False
