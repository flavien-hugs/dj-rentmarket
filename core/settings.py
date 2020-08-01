import os
import cloudinary
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
SECRET_KEY = get_env_variable(
    'SECRET_KEY', 'zb9g!qw2vat#pfkd16*ylu2b+*&mcf42#1)%qfr_4@6*f72heo')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = TEMPLATE_DEBUG = config('DEBUG', default=True, cast=bool)
DEFAULT_CHARSET = 'UTF-8'
DEFAULT_CONTENT_TYPE = 'text/html'
SITE_DESCRIPTION = 'Vous retrouverez tous ce dont\
    vous aurez besoin pour le quotidien'
META_KEYWORDS = 'shopping, location, ecommerce, accessories,\
    TV, Audio, smartphone, Mode, Electromenager'
ALLOWED_HOSTS = []
SITE_NAME = 'RentMarket'
LOCATION_SESSION_ID = 'cartsession'
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ' '

MANAGERS = (('flavien hugs', "flavienhgs@gmail.com"),)
ADMINS = MANAGERS

# USER MODEL
AUTH_USER_MODEL = 'accounts.User'
SITE_ID = 1

# Application definition
INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sitemaps',

    'widget_tweaks',
    'django_countries',
    'phonenumber_field',
    'phonenumbers',
    'django_user_agents',
    'django_social_share',
    'cloudinary',
    'compressor',

    'accounts.apps.AccountsConfig',
    'shop.apps.ShopConfig',
    'location.apps.LocationConfig',
    'address.apps.AddressConfig',
    'orders.apps.OrdersConfig',
    'payment.apps.PaymentConfig',
    'subscription.apps.SubscriptionConfig',

    'analytics.apps.AnalyticsConfig',

]

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',

    'django_user_agents.middleware.UserAgentMiddleware',
    'core.middleware.CoreMiddleware',
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
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.csrf',
                'django.contrib.messages.context_processors.messages',

                'core.context_processors.meta',
                'core.context_processors.category',
                'core.context_processors.location',
                'core.context_processors.featured_product',
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
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

# Compress Static files (CSS, JavaScript)
# https://django-compressor.readthedocs.io/en/latest/

COMPRESS_ENABLED = False
COMPRESS_CSS_HASHING_METHOD = 'content'
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]

HTML_MINIFY = True
KEEP_COMMENTS_ON_MINIFYING = True


LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'dashboard:dashboard'
LOGOUT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
FORCE_SESSION_TO_ONE = False
FORCE_INACTIVE_USER_ENDSESSION = False

# SENDGRID CONFIG
EMAIL_PORT = 587
EMAIL_USE_TLS = True
SENDGRID_API_KEY = config('SENDGRID_API_KEY', default='')
EMAIL_HOST = 'smtp-relay.sendinblue.com'
EMAIL_HOST_USER = 'flavienhgs@gmail.com'
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'RentMarket <info@rm.com>'
BASE_URL = ''
SESSION_COOKIE_SECURE = True

PHONENUMBER_DEFAULT_REGION = "CI"
PHONENUMBER_DB_FORMAT = "INTERNATIONAL"

# Name of cache backend to cache user agents. If it not specified default
# cache alias will be used. Set to `None` to disable caching.
USER_AGENTS_CACHE = 'default'


# Cloudinary settings for Django.
cloudinary.config(
    cloud_name='unsta',
    api_key='746746447688237',
    api_secret='dPGznYS0Ba02DQPjqzr5GBtfrSY',
    secure=True
)

# STRIPE PAYMENT
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
STRIPE_PUB_KEY = config('STRIPE_PUB_KEY')
