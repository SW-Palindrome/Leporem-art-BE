import os

from .base import *

AWS_STORAGE_BUCKET_NAME = 'leporem-art-media-dev'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db-leporemart-dev',
        'USER': 'palindrome',
        'PASSWORD': 'dikqU8-jyqjac-ruxxyf',
        'HOST': 'db.leporem.art',
        'PORT': '3306',
    }
}
