from storages.backends.s3boto3 import S3Boto3Storage





class StaticRootS3BotoStorage(S3Boto3Storage):
    location = 'lmsfolder/static'

class MediaRootS3BotoStorage(S3Boto3Storage):
    location = 'lmsfolder/media'