from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-*oatv!pap9uj=-8+5_#%n@71soz!f0&nnt0hn8y^%&x9m6-cag"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES = {
    'default': {
        'ENGINE': os.environ.get("SQL_ENGINE"),
        'NAME': os.environ.get("SQL_DATABASE"),
        'USER': os.environ.get("SQL_USER"),
        'PASSWORD': os.environ.get("SQL_PASSWORD"),  # yourpassword
        'HOST': os.environ.get("SQL_HOST"),  # Set to empty string for localhost.
        'PORT': os.environ.get("SQL_PORT"),  # Set to empty string for default.
    }
}

try:
    from .local import *
except ImportError:
    pass
