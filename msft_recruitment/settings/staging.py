from .base import *

DEBUG = False

ALLOWED_HOSTS = ['staging.yourdomain.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('STAGING_DB_NAME'),
        'USER': os.getenv('STAGING_DB_USER'),
        'PASSWORD': os.getenv('STAGING_DB_PASSWORD'),
        'HOST': os.getenv('STAGING_DB_HOST'),
        'PORT': os.getenv('STAGING_DB_PORT'),
    }
}