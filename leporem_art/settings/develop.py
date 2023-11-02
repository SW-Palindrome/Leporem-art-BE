import os

import boto3

from .base import *

AWS_STORAGE_BUCKET_NAME = 'leporem-art-media-dev'

DEBUG = True

ALLOWED_HOSTS = ['*']

# Load SSM
ssm = boto3.client("ssm", region_name="ap-northeast-2")

SECRET_KEY = ssm.get_parameter(Name='/leporem_art/settings/base/SECRET_KEY', WithDecryption=True)['Parameter']['Value']

# DATABASE 설정
param_db = ssm.get_parameter(Name='/leporem_art/settings/develop/DATABASES', WithDecryption=True)['Parameter']['Value']
json_db = json.loads(param_db)
DATABASES = {
    'default': {
        'ENGINE': json_db['ENGINE'],
        'NAME': json_db['NAME'],
        'USER': json_db['USER'],
        'PASSWORD': json_db['PASSWORD'],
        'HOST': json_db['HOST'],
        'PORT': json_db['PORT'],
    }
}

# APPLE Oauth Settings
param_apple = ssm.get_parameter(Name='/leporem_art/settings/base/APPLE_CONFIG', WithDecryption=True)['Parameter'][
    'Value'
]
json_apple = json.loads(param_apple)
APPLE_CONFIG = {
    'SOCIAL_AUTH_APPLE_ID_CLIENT': json_apple['SOCIAL_AUTH_APPLE_ID_CLIENT'],
    'SOCIAL_AUTH_APPLE_ID_SERVICE': json_apple['SOCIAL_AUTH_APPLE_ID_SERVICE'],
    'SOCIAL_AUTH_APPLE_ID_TEAM': json_apple['SOCIAL_AUTH_APPLE_ID_TEAM'],
    'SOCIAL_AUTH_APPLE_ID_KEY': json_apple['SOCIAL_AUTH_APPLE_ID_KEY'],
    'SOCIAL_AUTH_APPLE_ID_SECRET': json_apple['SOCIAL_AUTH_APPLE_ID_SECRET'],
    'SOCIAL_AUTH_APPLE_ID_SCOPE': json_apple['SOCIAL_AUTH_APPLE_ID_SCOPE'],
    'SOCIAL_AUTH_APPLE_ID_EMAIL_AS_USERNAME': json_apple['SOCIAL_AUTH_APPLE_ID_EMAIL_AS_USERNAME'],
    'SOCIAL_AUTH_APPLE_ID_PUBLIC': json_apple['SOCIAL_AUTH_APPLE_ID_PUBLIC'],
}

param_firebase = ssm.get_parameter(Name='/leporem_art/settings/base/FIREBASE_CONFIG', WithDecryption=True)['Parameter'][
    'Value'
]
FIREBASE_CONFIG = json.loads(param_firebase)
FIREBASE_MESSAGE_SEND_URL = f'https://fcm.googleapis.com/v1/projects/{FIREBASE_CONFIG["project_id"]}/messages:send'

# 배송 트래킹 설정 (스마트 택배 API)
param_delivery_tracking = ssm.get_parameter(Name='/leporem_art/settings/base/delivery-tracking', WithDecryption=True)[
    'Parameter'
]['Value']
DELIVERY_TRACKING_CONFIG = json.loads(param_delivery_tracking)
SMART_DELIVERY_TRACKING_API_URL = DELIVERY_TRACKING_CONFIG['DELIVERY_TRACKING_BASE_URL']
SMART_DELIVERY_TRACKING_API_KEY = DELIVERY_TRACKING_CONFIG['API_KEY']

boto3_log_client = boto3.client('logs')


AWS_LOG_GROUP = '/leporemart/api/dev'
AWS_LOGGER_NAME = 'watchtower-logger'  # your logger

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'aws': {
            # you can add specific format for aws here
            # if you want to change format, you can read:
            #    https://stackoverflow.com/questions/533048/how-to-log-source-file-name-and-line-number-in-python/44401529
            'format': u"%(asctime)s [%(levelname)-8s] %(message)s [%(pathname)s:%(lineno)d]",
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'watchtower': {
            'level': 'DEBUG',
            'class': 'watchtower.CloudWatchLogHandler',
            'log_group': AWS_LOG_GROUP,
            'formatter': 'aws',  # use custom format
        },
    },
    'loggers': {
        AWS_LOGGER_NAME: {
            'level': 'DEBUG',
            'handlers': ['watchtower'],
            'propagate': False,
        },
        # add your other loggers here...
    },
}
