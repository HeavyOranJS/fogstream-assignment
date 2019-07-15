"""
Django settings for fogstreamTest project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import json
from django.core.exceptions import ImproperlyConfigured

#NOTE: structure of config.json you can find in dummy.config.json

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#open config.json with secret info
with open(os.path.join(BASE_DIR, 'fogstreamTest/config.json')) as config_file:
    CONFIG = json.load(config_file)

def get_config(setting, config=CONFIG):
    """
    Get secret setting from config.json or fail with ImproperlyConfigured
    """
    try:
        return config[setting]
    except KeyError:
        raise ImproperlyConfigured("Set the {} setting".format(setting))

#TODO: CHECK DEPLOY BEFORE PRODUCTION
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

SECRET_KEY = get_config('SECRET_KEY')

#TODO: TURN OFF BEFORE PRODUCTION
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'assignment.apps.AssignmentConfig',
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

ROOT_URLCONF = 'fogstreamTest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'fogstreamTest.wsgi.application'

#NAME and USER taken out to config.json because there is no reason
#for you to create table and user with my DB_NAME and DB_USER
DATABASES = {
    'default':
    {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':  get_config('DB_NAME'),
        'USER': get_config('DB_USER'),
        'PASSWORD': get_config('DB_KEY'),
        'HOST': 'localhost',
        'PORT': '5432',
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Vladivostok'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'

#I think admin's email should not be public
ADMINS = [('Admin', get_config("EMAIL_ADMIN"))]

#Email settings
EMAIL_USE_TLS = True
#I used gmail, so HOST_USER should be *gmail.com
EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_HOST_USER = get_config('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = get_config('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = 'fogtest'

DEFAULT_TO_EMAIL = 'some_examplar_email@fogtest.com'
