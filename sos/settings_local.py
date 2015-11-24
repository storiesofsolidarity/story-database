from settings import *

DEBUG = True

#Local settings only
SSLIFY_DISABLE = True
CORS_ORIGIN_ALLOW_ALL = True

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
MEDIA_URL = 'http://localhost:8000/media/'

SECRET_KEY = 'prej4faf6vum6resh5foa8hai9wat4ca'
