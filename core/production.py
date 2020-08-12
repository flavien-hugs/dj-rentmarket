# -*- coding: utf-8 -*-
# core/production.py

import django_heroku
import dj_database_url
from core.settings import *

DEBUG = TEMPLATE_DEBUG = False
COMPRESS_ENABLED = False
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
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'csp.middleware.CSPMiddleware',
]

# Keep our policy as strict as possible
# Content Security Policy
"""CSP_DEFAULT_SRC = ("'none'", )
CSP_CONNECT_SRC = ("'self'", )
CSP_OBJECT_SRC = ("'none'", )
CSP_BASE_URI = ("'none'", )
CSP_FRAME_ANCESTORS = ("'none'", )
CSP_FORM_ACTION = ("'self'", )
CSP_INCLUDE_NONCE_IN = ('script-src',)"""

# https://docs.djangoproject.com/fr/3.0/ref/settings/
# Let's Encrypt ssl/tls https

HOST_SCHEME = "https://"
X_FRAME_OPTIONS = 'DENY'
SECURE_FRAME_DENY = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_PRELOAD = True
USE_X_FORWARDED_HOST = True
SECURE_HSTS_SECONDS = 15768000
SECURE_BROWSER_XSS_FILTER = True
CORS_REPLACE_HTTPS_REFERER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_HOST = 'https://rtmarket.herokuapp.com'
SECURE_REFERRER_POLICY = 'origin-when-cross-origin'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Activate Django-Heroku.
django_heroku.settings(locals())

# EMAIL SENDER
EMAIL_SUBJECT_PREFIX = '[RENTMARKET]'
