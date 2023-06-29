from .common import *
import dj_database_url

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p3gm=o9o+_r(5*o$$kn#h*8#n1r)aquf^^nm_v5u0pn^qa$=4*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['https://planet-frontend.dev.altix.co/', 'https:/www.pl4n3t.com', '*']
CSRF_TRUSTED_ORIGINS = ['https://pl4n3t.com', 'https://www.pl4n3t.com', 'https://planet-frontend.dev.altix.co']

# CORS Config: install django-cors-headers and uncomment the following to allow CORS from any origin
"""
DEV_APPS = [
    'corsheaders'
]

INSTALLED_APPS += DEV_APPS

DEV_MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware'
]

MIDDLEWARE = MIDDLEWARE + DEV_MIDDLEWARE  # CORS middleware should be at the top of the list

CORS_ORIGIN_ALLOW_ALL = True
"""

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# Configured with DATABASE_URL env, usually from dokku
if os.environ.get('DATABASE_URL', ''):
    DATABASES = {
        'default': dj_database_url.config(),
    }
    DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'db',
            'PORT': 5432,
        }
    }


# Local settings
try:
    from .temp import *
except ImportError:
    pass

# Simple JWT
SIMPLE_JWT.update({
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'SIGNING_KEY': SECRET_KEY,
})


# Webpack config
WEBPACK_LOADER['DEFAULT'].update({
    'BUNDLE_DIR_NAME': 'webpack_bundles/',  # must end with slash
    'STATS_FILE': os.path.join(BASE_DIR, 'webpack-development-stats.json'),
})

EMAIL_HOST = os.environ.setdefault('EMAIL_HOST', '')
EMAIL_PORT = os.environ.setdefault('EMAIL_PORT', '')
EMAIL_HOST_USER = os.environ.setdefault('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.setdefault('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = True
