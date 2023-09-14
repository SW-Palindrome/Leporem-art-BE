from .base import *

AWS_STORAGE_BUCKET_NAME = 'leporem-art-media-dev'

DEBUG = True
ALLOWED_HOSTS = []

# Load SSM
ssm = boto3.client("ssm", region_name="ap-northeast-2")

# DATABASE 설정
param_db = ssm.get_parameter(Name='/leporem_art/settings/develop/DATABASES', WithDecryption=True)['Parameter']['Value']
DATABASES = {'default': {}}
[DATABASES['default'].setdefault(i.split(':')[0], i.split(':')[1]) for i in param_db.split('\n') if i != '']
