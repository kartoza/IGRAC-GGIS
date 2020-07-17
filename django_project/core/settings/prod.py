# coding=utf-8

"""Project level settings."""
from .base import *  # noqa

# Comment if you are not running behind proxy
USE_X_FORWARDED_HOST = True

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = True

# See fig.yml file for postfix container definition#
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Host for sending e-mail.
EMAIL_HOST = 'smtp'
# Port for sending e-mail.
EMAIL_PORT = 25
# SMTP authentication information for EMAIL_HOST.
# See fig.yml for where these are defined
EMAIL_HOST_USER = 'noreply@kartoza.com'
EMAIL_HOST_PASSWORD = 'docker'
EMAIL_USE_TLS = False
EMAIL_SUBJECT_PREFIX = '[IGRAC-GGIS]'

SERVER_EMAIL = os.environ.get('ADMIN_EMAILS', 'admin@kartoza.com')
DEFAULT_FROM_EMAIL = os.environ.get('ADMIN_EMAILS', 'admin@kartoza.com')
