import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['reference.examply.tyu']

LOCAL_SETTINGS = False


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'example_reference',
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': 'db',
    }
}


# PASSPORT
PASSPORT_URL = "https://passport.examply.tyu"
PASSPORT_SESSION_ID_NAME = "passport_session_id"
PASSPORT_SECRET_KEY = "{0}passport".format(SECRET_KEY)
MAIN_DOMAIN = 'examply.tyu'
APP_SUBDOMAIN = 'reference.{0}'.format(MAIN_DOMAIN)
PASSPORT_USER_CREDENTIALS_URI = 'https://passport.{0}/auth/data'.format(MAIN_DOMAIN)
# ===============================