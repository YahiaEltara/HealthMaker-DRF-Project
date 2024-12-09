from .base import *
from . import get_secret



DEBUG = False
ALLOWED_HOSTS = ['*']

# Change DATABASES to connect to a real database
DB_NAME = get_secret("DB_NAME")
DB_USER_NM = get_secret("DB_USER_NM")
DB_USER_PW = get_secret("DB_USER_PW")
DB_IP = get_secret("DB_IP")
DB_PORT = get_secret("DB_PORT")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER_NM,
        "PASSWORD": DB_USER_PW,
        "HOST": DB_IP,
        "PORT": DB_PORT,
    }
}
