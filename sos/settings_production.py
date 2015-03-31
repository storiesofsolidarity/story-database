import os
import dj_database_url
from memcacheify import memcacheify

from settings import *

DEBUG = False
TEMPLATE_DEBUG = False

DATABASES['default'] =  dj_database_url.config()
CACHES = memcacheify()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allowed host headers
ALLOWED_HOSTS = ['.storiesofsolidarity.org','sos-data-api.herokuapp.com']
CORS_ORIGIN_WHITELIST = ALLOWED_HOSTS

# Share session cookies with frontend
# SESSION_COOKIE_DOMAIN = '.storiesofsolidarity.org'

# Static asset configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)