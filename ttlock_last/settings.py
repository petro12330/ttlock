import os
from pathlib import Path
from decouple import config
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "ttlock"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ttlock_last.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ttlock_last.wsgi.application'

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
            'OPTIONS': {
                'timeout': 20,  # in seconds
                # see also
                # https://docs.python.org/3.7/library/sqlite3.html#sqlite3.connect
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': config("ENGINE", None),
            'NAME': config("NAME", None),
            'USER': config("USER", None),
            'PASSWORD': config("PASSWORD", None),
            'HOST': config("HOST", None),
            'PORT': config("PORT", None),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join("", "static"),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django
# Адрес прилоджения. В локальной разработке "http://127.0.0.1:8000/"
BASE_URL_ADDRESS = config("BASE_URL_ADDRESS")
USERNAME_ADMIN = config("USERNAME_ADMIN")
PASSWORD_ADMIN = config("PASSWORD_ADMIN")

# UDS
UDS_COMPANY_ID = config("UDS_COMPANY_ID")
UDS_API_KEY = config("UDS_API_KEY")
UDS_API_URL = config("UDS_API_URL")

# CHAT_2_DECK
CHAT_2_DECK_URL = config("CHAT_2_DECK_URL")
CHAT_2_DECK_TOKEN = config("CHAT_2_DECK_TOKEN")
PHONE_FOR_TEST = config("PHONE_FOR_TEST", None)

# HOLIHOP
HOLIHOP_API_KEY = config("HOLIHOP_API_KEY")
HOLIHOP_API_URL = config("HOLIHOP_API_URL")

# TTLOCK
TTLOCK_API_URI = config("TTLOCK_API_URI")

# Sentry
if not DEBUG:
    sentry_sdk.init(
        dsn=config("SENTRY_URL"),
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True
    )