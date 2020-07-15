# -*- coding: utf-8 -*-
"""Settings for when running under docker in development mode."""
from .dev import *  # noqa

ALLOWED_HOSTS = ['*']
USE_X_FORWARDED_HOST = True

ADMINS = (
    ('Anita Hapsari', 'anita@kartoza.com'),
)

# Set debug to True for development
DEBUG = True
TEMPLATE_DEBUG = DEBUG
LOGGING_OUTPUT_ENABLED = DEBUG
LOGGING_LOG_SQL = DEBUG

DATABASES = {
    'default': {
        'NAME': 'geonode',
        'USER': 'geonode',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
        'CONN_MAX_AGE': 5,
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'OPTIONS': {'options': '-c search_path=groundwater,public', 'connect_timeout': 5}},
    'datastore': {
        'NAME': 'geonode_data',
        'USER': 'geonode_data',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
        'CONN_MAX_AGE': 5,
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'OPTIONS': {'options': '-c search_path=groundwater,public', 'connect_timeout': 5}}
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'cache:11211',
    }
}
