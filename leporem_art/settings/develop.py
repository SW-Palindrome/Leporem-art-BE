import os

from .base import *

AWS_STORAGE_BUCKET_NAME = 'leporem-art-media-dev'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db-leporemart',
        'USER': 'palindrome',
        'PASSWORD': 'dikqU8-jyqjac-ruxxyf',
        'HOST': 'leporem-art-db.ckbfh3nhrtug.ap-northeast-2.rds.amazonaws.com',
        'PORT': '3306',
    }
}
