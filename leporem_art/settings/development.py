from .base import *

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db-leporemart',
        'USER': 'palindrome',
        'PASSWORD': 'dikqU8-jyqjac-ruxxyf',
        'HOST': 'db-leporemart.cadfwurpcjgm.ap-northeast-2.rds.amazonaws.com',
        'PORT': '3306',
    }
}