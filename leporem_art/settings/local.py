from .base import *

AWS_STORAGE_BUCKET_NAME = 'leporem-art-media-dev'

DEBUG = True
ALLOWED_HOSTS = []

# Load SSM
ssm = boto3.client("ssm", region_name="ap-northeast-2")

SECRET_KEY = ssm.get_parameter(Name='/leporem_art/settings/base/SECRET_KEY', WithDecryption=True)['Parameter']['Value']

# DATABASE 설정
param_db = ssm.get_parameter(Name='/leporem_art/settings/develop/DATABASES', WithDecryption=True)['Parameter']['Value']
DATABASES = {'default': {}}
[DATABASES['default'].setdefault(i.split(':')[0], i.split(':')[1]) for i in param_db.split('\n') if i != '']

# APPLE Oauth Settings
param_apple = ssm.get_parameter(Name='/leporem_art/settings/base/APPLE_CONFIG', WithDecryption=True)['Parameter'][
    'Value'
]
APPLE_CONFIG = {}
[APPLE_CONFIG.setdefault(i.split(':')[0], i.split(':')[1]) for i in param_apple.split(',\n') if i != '']

# APPLE Oauth Settings
param_apple = ssm.get_parameter(Name='/leporem_art/settings/base/APPLE_CONFIG', WithDecryption=True)['Parameter'][
    'Value'
]
APPLE_CONFIG = {}
[APPLE_CONFIG.setdefault(i.split(':')[0], i.split(':')[1]) for i in param_apple.split(',\n') if i != '']
