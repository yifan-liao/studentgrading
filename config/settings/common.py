"""
Django settings for mysite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from __future__ import absolute_import, unicode_literals

import environ

ROOT_DIR = environ.Path(__file__) - 3  # (/a/b/myfile.py - 3 = /)
APPS_DIR = ROOT_DIR.path('studentgrading')

env = environ.Env()
environ.Env.read_env(str(ROOT_DIR) + '/.env')

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    # 'django.contrib.humanize',

    # Admin
    'django.contrib.admin',
)
THIRD_PARTY_APPS = (
    'crispy_forms',  # Form layouts
    'rest_framework',
    'guardian',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    # custom apps go here
    'studentgrading.users',  # users app
    'studentgrading.core',   # core app
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool("DJANGO_DEBUG", False)

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
'''
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)
'''

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
# EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
'''
ADMINS = (
    ("""Yifan Y Liao""", 'szlyyfgm@gmail.com'),
)
'''

# MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# environ does not support oracle db
def get_db_setting_str(env_var):
    if env(env_var).split(':')[0] == 'oracle':
        setting = env.db(env_var, engine='django.db.backends.oracle')
        setting['PORT'] = str(setting['PORT'])
        return setting
    return env.db(env_var)

DATABASES = {
    # oracle db setting
    # 'default': env.db('DATABASE_URL', engine='django.db.backends.oracle')
    'default': get_db_setting_str('DATABASE_URL')
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # Your stuff: custom template context processors go here
            ],
        },
    },
]

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
STATIC_ROOT = str(ROOT_DIR('studentgrading/'))

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
)

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
MEDIA_ROOT = str(APPS_DIR('media'))

MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = 'core:redirect'
LOGIN_URL = 'core:login'

# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = r'^admin/'

# REST Framework Configuration
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    )
}

# django-guardian Configuration
# ------------------------------------------------------------------------------
ANONYMOUS_USER_ID = -1
GUARDIAN_MONKEY_PATCH = False
