import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

AWS_STORAGE_BUCKET_NAME = 'leporem-art-media-prod'

DEBUG = True
ALLOWED_HOSTS = ['*']

# Load SSM
ssm = boto3.client("ssm", region_name="ap-northeast-2")

# Sentry 설정
dsn = ssm.get_parameter(Name='/leporem_art/settings/production/sentry', WithDecryption=True)['Parameter']['Value']

sentry_sdk.init(
    dsn=dsn,
    integrations=[DjangoIntegration()],
    auto_session_tracking=False,
    traces_sample_rate=0,
)

SECRET_KEY = ssm.get_parameter(Name='/leporem_art/settings/base/SECRET_KEY', WithDecryption=True)['Parameter']['Value']

# DATABASE 설정
param_db = ssm.get_parameter(Name='/leporem_art/settings/production/DATABASES', WithDecryption=True)['Parameter'][
    'Value'
]
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

# Firebase Admin SDK setup
param_firebase = ssm.get_parameter(Name='/leporem_art/settings/base/FIREBASE_CONFIG', WithDecryption=True)['Parameter'][
    'Value'
]
FIREBASE_CONFIG = json.loads(param_firebase)
cred = credentials.Certificate(FIREBASE_CONFIG)
firebase_admin.initialize_app(cred)
