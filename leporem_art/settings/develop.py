import os

from .base import *

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
S3_BUCKET_NAME = "leporem-art-backend-static"
STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"
AWS_S3_BUCKET_NAME_STATIC = S3_BUCKET_NAME
AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % S3_BUCKET_NAME
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
