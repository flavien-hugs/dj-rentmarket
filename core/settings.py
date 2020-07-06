import os
from decouple import config
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name, default_value=None):
    try:
        return os.environ[var_name]
    except KeyError:
        if default_value is None:
            error_msg = "Set the {} environment variable".format(var_name)
            raise ImproperlyConfigured(error_msg)
        else:
            return default_value

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable('SECRET_KEY', 'zb9g!qw2vat#pfkd16*ylu2b+*&mcf42#1)%qfr_4@6*f72heo')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = TEMPLATE_DEBUG = True
DEFAULT_CHARSET = 'UTF-8'
DEFAULT_CONTENT_TYPE = 'text/html'
SITE_DESCRIPTION = ''
META_KEYWORDS = ''
ALLOWED_HOSTS = []
SITE_NAME = 'Rent Market'
LOCATION_SESSION_ID = 'cartsession'
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ' '
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # 'cloudinary_storage',
    # 'cloudinary',

    'widget_tweaks',
    'django_countries',
    'phonenumber_field',
    'django_user_agents',

    'accounts.apps.AccountsConfig',
    'shop.apps.ShopConfig',
    'location.apps.LocationConfig',
    'orders.apps.OrdersConfig',
    'subscription.apps.SubscriptionConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

ROOT_URLCONF = 'core.urls'

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
                'django.template.context_processors.i18n',
                'django.template.context_processors.csrf',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.location',
                'core.context_processors.category',
            ],

            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    'OPTIONS': {'max_similarity': 0.9,}},
    {
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    'OPTIONS': {'min_length': 9,}
    },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# PASSWORD HASHERS
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'fr'
TIME_ZONE = 'UTC'
USE_I18N = USE_L10N = USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

LOGIN_URL = 'accounts:login'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_REDIRECT_URL = 'dashboard:dashboard'

# Cloudinary settings for Django. Add to your settings file.
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUD_NAME'),
    'API_KEY': config('API_KEY'),
    'API_SECRET': config('API_SECRET'),
}

EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)

PHONENUMBER_DEFAULT_REGION = "CI"
PHONENUMBER_DB_FORMAT = "INTERNATIONAL"

# Name of cache backend to cache user agents. If it not specified default
# cache alias will be used. Set to `None` to disable caching.
USER_AGENTS_CACHE = 'default'
