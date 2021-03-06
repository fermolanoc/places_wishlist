"""
Django settings for wishlist project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from google.oauth2 import service_account
import os
from pathlib import Path
import mimetypes
mimetypes.add_type("text/css", ".css", True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!tagx-paxxqx7_qk4baylzjncq(k@#b%x04vy7i7k-^m)_bn4d'

# SECURITY WARNING: don't run with debug turned on in production!
if os.getenv('GAE_INSTANCE'):
    DEBUG = False
else:
    DEBUG = True


ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'travel_wishlist'
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

ROOT_URLCONF = 'wishlist.urls'

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

WSGI_APPLICATION = 'wishlist.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'places',
        'USER': 'fermolanoc',
        'PASSWORD': os.getenv('GCP_DB_PW'),
        'HOST': '/cloudsql/travel-wishlist-332114:us-central1:wishlist-db',
        'PORT': '5432'
    }
}


# When locally, run on this port
if not os.getenv('GAE_INSTANCE'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# Specify a location to copy static files to when running python manage.py collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'www', 'static')


# Where in the file system to user_uploaded files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if os.getenv('GAE_INSTANCE'):
    GS_STATIC_FILE_BUCKET = 'travel-wishlist-332114.appspot.com'
    STATIC_URL = f'https://storage.cloud.google.com/{GS_STATIC_FILE_BUCKET}/static/'

    GS_BUCKET_NAME = 'wishlist-places-images'
    MEDIA_URL = f'https://storage.cloud.google.com/{GS_BUCKET_NAME}/media/'

    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        'travel-credentials.json')
else:
    # Media URL, for user-created media - becomes part of URL when images are displayed
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
