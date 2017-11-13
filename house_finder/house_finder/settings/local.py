from .base import *  # noqa

DEBUG = True

INSTALLED_APPS += ['behave_django', ]  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')  # noqa,
    }
}  # noqa
