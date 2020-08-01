# -*- coding: utf-8 -*-
# core/production.py

import django_heroku
import dj_database_url
from core.settings import *

DEBUG = TEMPLATE_DEBUG = False
BASE_URL = 'https://rtmarket.herokuapp.com'
ALLOWED_HOSTS = ['.herokuapp.com']

# Parse database configuration from $DATABASE_URL
# Change 'default' database configuration with
# $DATABASE_URL.
DATABASES['default'].update(
    dj_database_url.config(
        conn_max_age=500,
        ssl_require=True)
    )

# APPLICATION DEFINITION
INSTALLED_APPS += ['whitenoise.runserver_nostatic']

# 'django.middleware.security.SecurityMiddleware',
MIDDLEWARE += [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]


# Let's Encrypt ssl/tls https
HOST_SCHEME = "https://"
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SECURE = True
USE_X_FORWARDED_HOST = True
CORS_REPLACE_HTTPS_REFERER = True

SECURE_FRAME_DENY = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 1000000
SECURE_BROWSER_XSS_FILTER = True
SECURE_REFERRER_POLICY = 'origin'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Activate Django-Heroku.
django_heroku.settings(locals())
