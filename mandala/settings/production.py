from .base import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://0aafcd76b5acee144db02675651e9073@o658296.ingest.sentry.io/4505797333221376",
    integrations=[DjangoIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

DEBUG = False
SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = [
    "polyglotmandala.com",
    "www.polyglotmandala.com",
    config("SERVER_IP"),
    "localhost",
]

# AWS settings
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

INSTALLED_APPS = INSTALLED_APPS + [
    # AWS
    "storages",
]

CSRF_TRUSTED_ORIGINS = [
    "https://www.polyglotmandala.com",
    "http://www.polyglomandala.com",
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        }
    },
    'handlers': {
        'file': {
            'level': config('DJANGO_LOG_LEVEL', default='ERROR'),
            'class': 'logging.FileHandler',
            'filename': config("LOGGING_PATH"),
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': config('DJANGO_LOG_LEVEL', default='ERROR'),
            'propagate': True,
        },
            'django.request': {
            'handlers': ['file'],
            'level': config('DJANGO_REQUEST_LOG_LEVEL', default='ERROR'),
            'propagate': True,
        },
        'django.template': {
            'level': config('DJANGO_LOG_LEVEL', default='ERROR'),
            'handlers': ['file'],
            'propagate': True,
            },
        'core': {
            'handlers': ['file'],
            'level': config('ACCOUNTS_LOG_LEVEL', default='ERROR'),
            'propagate': True,
        },
        'home': {
            'handlers': ['file'],
            'level': config('HOME_LOG_LEVEL', default='ERROR'),
            'propagate': True,
        },
    },
}

try:
    from .local import *
except ImportError:
    pass
