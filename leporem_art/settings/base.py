"""
Django settings for leporem_art project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from datetime import timedelta
from pathlib import Path

import pymysql

pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-hs5l-zi%l-ojy3gpjml!5snrnh@^bd*y887jn9ut(6cla7e$#6"

# SECURITY WARNING: don't run with debug turned on in production!

# DEBUG = True

# ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django_extensions',
    'django_filters',
    'rest_framework',
    'corsheaders',
    'apps.buyers',
    'apps.chats',
    'apps.orders',
    'apps.users',
    'apps.sellers',
    'apps.items',
    "dj_rest_auth",
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "leporem_art.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "leporem_art.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.users.authentications.OIDCAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
}

CORS_ALLOW_ALL_ORIGINS = True

# 스태프용 ID 토큰 및 계정
TEST_ID_TOKEN = 'Leporemart33!'
TEST_STAFF_NICKNAME = '공예쁨'

# Django Storage Settings
STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
    },
}

# Payload Max Size
DATA_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024

# Setting AWS_QUERYSTRING_AUTH to False removes query parameter authentication from generated URLs.
# https://django-storages.readthedocs.io/en/1.5.0/backends/amazon-S3.html
AWS_QUERYSTRING_AUTH = False

APPLE_CONFIG = {
    'SOCIAL_AUTH_APPLE_ID_CLIENT': 'leporemart.palindrome.com',  # Your client_id com.application.your, aka "Service ID"
    'SOCIAL_AUTH_APPLE_ID_TEAM': 'BH6CVTK388',  # Your Team ID, ie K2232113
    'SOCIAL_AUTH_APPLE_ID_KEY': '8FM8MZ2XUC',  # Your Key ID, ie Y2P99J3N81K
    'SOCIAL_AUTH_APPLE_ID_SECRET': """
-----BEGIN PRIVATE KEY-----
MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgVElWMtuZjXsfCBIR
Mv3Ims/BSOlGpQL6KUeLp/DuOqigCgYIKoZIzj0DAQehRANCAATs5MXLjb0XmSAw
oz66KYyu8BsHEhSaAoCKr99t3y2xA7vHT3MhyT46h2XwmFxFI2WuqNeJ79rxPbIU
vhDfYYmI
-----END PRIVATE KEY-----
    """,
    'SOCIAL_AUTH_APPLE_ID_SCOPE': 'email, name',
    'SOCIAL_AUTH_APPLE_ID_EMAIL_AS_USERNAME': True,  # If you want to use email as username
    'SOCIAL_AUTH_APPLE_ID_PUBLIC': "1JiU4l3YCeT4o0gVmxGTEK1IXR-Ghdg5Bzka12tzmtdCxU00ChH66aV-4HRBjF1t95IsaeHeDFRgmF0lJbTDTqa6_VZo2hc0zTiUAsGLacN6slePvDcR1IMucQGtPP5tGhIbU-HKabsKOFdD4VQ5PCXifjpN9R-1qOR571BxCAl4u1kUUIePAAJcBcqGRFSI_I1j_jbN3gflK_8ZNmgnPrXA0kZXzj1I7ZHgekGbZoxmDrzYm2zmja1MsE5A_JX7itBYnlR41LOtvLRCNtw7K3EFlbfB6hkPL-Swk5XNGbWZdTROmaTNzJhV-lWT0gGm6V1qWAK2qOZoIDa_3Ud0Gw",
}

AUTHENTICATION_BACKENDS = [
    "social_core.backends.oauth",
    "social_core.backends.apple.AppleIdAuth",
]

JWT_AUTH = {
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALGORITHM': 'HS256',
    'JWT_ALLOW_REFRESH': True,
}
