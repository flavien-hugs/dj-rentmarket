# -*- coding: utf-8 -*-
# core/production.py

import django_heroku
import dj_database_url
from core.settings import *

DEBUG = TEMPLATE_DEBUG = False

# Parse database configuration from $DATABASE_URL
# Change 'default' database configuration with $DATABASE_URL.
DATABASES['default'].update(
    dj_database_url.config(
        conn_max_age=500,
        ssl_require=True))

# APPLICATION DEFINITION
INSTALLED_APPS += ['whitenoise.runserver_nostatic']

# 'django.middleware.security.SecurityMiddleware',
MIDDLEWARE += [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

HOST_SCHEME = "https://"
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SECURE = True
USE_X_FORWARDED_HOST = True
SESSION_COOKIE_SECURE = False
CORS_REPLACE_HTTPS_REFERER = False

SECURE_FRAME_DENY = False
SECURE_HSTS_SECONDS = 3600
SECURE_SSL_REDIRECT = False
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_REFERRER_POLICY = 'origin'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Activate Django-Heroku.
django_heroku.settings(locals())
