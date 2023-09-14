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

# DATABASE 설정
param_db = ssm.get_parameter(Name='/leporem_art/settings/production/DATABASES', WithDecryption=True)['Parameter'][
    'Value'
]
DATABASES = {'default': {}}
[DATABASES['default'].setdefault(i.split(':')[0], i.split(':')[1]) for i in param_db.split('\n') if i != '']
