# -*- coding: utf-8 -*-
'''
Local settings

- Run in Debug mode
- Add Django Debug Toolbar
'''

from config.settings.common import *
import pymysql
pymysql.install_as_MySQLdb()

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES_DEBUG = DEBUG
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# Note: This key only used for development and testing.
SECRET_KEY = env("SECRET_KEY")

# django-debug-toolbar
# ------------------------------------------------------------------------------
# MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
# INSTALLED_APPS += ('debug_toolbar', )

