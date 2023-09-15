import os

from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db-leporemart-test',
        'USER': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

SECRET_KEY = ""
APPLE_CONFIG = ""
dsn = ""
