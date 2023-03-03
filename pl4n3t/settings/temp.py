from .common import *

SPECTACULAR_SETTINGS['SERVERS'] = [{"url": "http://localhost:8000"}]
DEBUG = True

BASE_URL = 'http://localhost:8000/'
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

ALLOWED_HOSTS = ["http://localhost:8000", '*']
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", 'https://pl4n3t.com', 'https://www.pl4n3t.com']
