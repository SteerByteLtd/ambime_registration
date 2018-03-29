import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

ALLOWED_HOSTS = ['ambime.co.uk', '35.176.109.71', 'localhost', '127.0.0.1']

INSTALLED_APPS = (
    'ambime',
    'main',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'import_export'
)
AUTH_USER_MODEL = 'main.User'
DEBUG = True

WSGI_APPLICATION = 'ambime.wsgi.application'

SECRET_KEY = 'ambime_website'

SITE_ID = 1

ROOT_URLCONF = 'ambime.urls_default'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ambime',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '35.176.109.71',
        'PORT': '5432'
    },
}

ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_EMAIL_SUBJECT_PREFIX = '[Ambime]'
SEND_ACTIVATION_EMAIL = True
REGISTRATION_AUTO_LOGIN = False
INCLUDE_AUTH_URLS = True
LOGIN_REDIRECT_URL = 'profile'

EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'noreply@ambime.co.uk'
EMAIL_HOST_PASSWORD = 'TerryDapo'
DEFAULT_FROM_EMAIL = 'noreply@ambime.co.uk'