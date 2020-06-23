# -*- coding: utf-8 -*-
# core/production.py

import dj_database_url
from core.settings import *

DEBUG = TEMPLATE_DEBUG = False

# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()

# APPLICATION DEFINITION
INSTALLED_APPS += ['whitenoise.runserver_nostatic']

# 'django.middleware.security.SecurityMiddleware',
MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']

ALLOWED_HOSTS = ['rentlocation.herokuapp.com']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
