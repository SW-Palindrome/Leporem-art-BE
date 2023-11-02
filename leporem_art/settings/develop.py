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

boto3_logs_client = boto3.client('logs')


AWS_LOG_GROUP = '/leporemart/api/dev'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'DEBUG',
        # Adding the watchtower handler here causes all loggers in the project that
        # have propagate=True (the default) to send messages to watchtower. If you
        # wish to send only from specific loggers instead, remove "watchtower" here
        # and configure individual loggers below.
        'handlers': ['watchtower', 'console'],
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'watchtower': {
            'class': 'watchtower.CloudWatchLogHandler',
            'boto3_client': boto3_logs_client,
            'log_group_name': AWS_LOG_GROUP,
            # Decrease the verbosity level here to send only those logs to watchtower,
            # but still see more verbose logs in the console. See the watchtower
            # documentation for other parameters that can be set here.
            'level': 'DEBUG',
        },
    },
    'loggers': {
        # In the debug server (`manage.py runserver`), several Django system loggers cause
        # deadlocks when using threading in the logging handler, and are not supported by
        # watchtower. This limitation does not apply when running on production WSGI servers
        # (gunicorn, uwsgi, etc.), so we recommend that you set `propagate=True` below in your
        # production-specific Django settings file to receive Django system logs in CloudWatch.
        'django.server': {'level': 'DEBUG', 'handlers': ['watchtower'], 'propagate': True},
        # Add any other logger-specific configuration here.
    },
}
