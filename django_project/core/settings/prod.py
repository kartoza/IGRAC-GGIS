# coding=utf-8
"""Project level settings."""

from .base import *  # noqa

# Comment if you are not running behind proxy
USE_X_FORWARDED_HOST = True

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False

# See fig.yml file for postfix container definition#
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Host for sending e-mail.
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp')
# Port for sending e-mail.
EMAIL_PORT = ast.literal_eval(os.environ.get('EMAIL_PORT', '25'))
# SMTP authentication information for EMAIL_HOST.
# See fig.yml for where these are defined
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'noreply@kartoza.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'docker')
EMAIL_USE_TLS = ast.literal_eval(os.environ.get('EMAIL_USE_TLS', 'False'))
EMAIL_USE_SSL = ast.literal_eval(os.environ.get('EMAIL_USE_SSL', 'False'))
EMAIL_SUBJECT_PREFIX = os.environ.get('EMAIL_SUBJECT_PREFIX', '[IGRAC-GGIS]')

SERVER_EMAIL = os.environ.get('ADMIN_EMAIL', 'noreply@kartoza.com')
DEFAULT_FROM_EMAIL = os.environ.get(
    'DEFAULT_FROM_EMAIL', 'noreply@kartoza.com'
)

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

CELERY_BEAT_SCHEDULE['run_all_harvester'] = {
    'task': 'gwml2.tasks.harvester.run_all_harvester',
    'schedule': crontab(minute=0, hour=00, day_of_week=[0, 3]),
}
