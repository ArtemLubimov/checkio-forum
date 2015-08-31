import os

from .django import BASE_DIR
from spirit.settings import *  # noqa


DOMAIN = 'forum.empireofcode.com'

ALLOWED_HOSTS = ['forum.empireofcode.com']

INSTALLED_APPS.extend([
    'loginas',
    'social.apps.django_app.default',

    'checkio_forum.libs.spirit_email_notification',
])

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'checkio_forum.libs.social.backends.auth.CheckiOOAuth2',
)

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'static_checkio'),
)

USE_I18N = False

USE_L10N = False
