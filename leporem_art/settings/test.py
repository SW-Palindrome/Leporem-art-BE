import os

from .base import *

AWS_STORAGE_BUCKET_NAME = 'leporem-art-media-test'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db-leporemart-test',
        'USER': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
