import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_-r1_+g$f*zu5-v6vo*#(l!zmlgx#dvyf0qd#+-od*a@gdweih'

DEBUG = False
SYNC_MODE = os.getenv('SYNC_MODE', 'false') == 'true'

ALLOWED_HOSTS = [
    '0.0.0.0',
    '127.0.0.1',
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'django_json_widget',
    # 'django_celery_results',  # NOQA TODO: Turn back when it will be compatible with Celery 5.*
    # 'django_celery_beat',  # NOQA TODO: Turn back when beat will be compatible with Celery 5.*
    'configuration',
    'message_producers',
    'message_consumers',
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

ROOT_URLCONF = 'notifier.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'notifier.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_SCHEMA', 'notifier'),
        'USER': os.environ.get('DB_USER', 'notifier'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'notifier'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'configuration.User'

# Celery configs
# TODO: Move to their own configfile

CELERY_BROKER_URL = os.getenv('CELERY_BROKER', 'amqp://notifier:notifier@rabbitmq:5672/notifier')
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'max_retries': 3,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.5,
}

USE_GRAPHIQL_INTERFACE = True

GRAPHENE = {
    'SCHEMA': 'notifier.schema.schema',
}

SENTRY_DSN = os.getenv('SENTRY_DSN', None)

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)

try:
    from .local_settings import *  # noqa
except ImportError:
    pass
