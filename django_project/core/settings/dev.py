from .base import *  # noqa

DATABASES = {
    'default': {
        'NAME': 'geonode',
        'USER': 'geonode',
        'PASSWORD': 'geonode',
        'HOST': 'postgres',
        'PORT': 5432,
        'CONN_MAX_AGE': 5,
        'ENGINE': 'django.contrib.gis.db.backends.postgis'},
    'datastore': {
        'NAME': 'geonode_data',
        'USER': 'geonode_data',
        'PASSWORD': 'geonode',
        'HOST': 'postgres',
        'PORT': 5432,
        'CONN_MAX_AGE': 5,
        'ENGINE': 'django.contrib.gis.db.backends.postgis'},
    'gwml2': {
        'NAME': 'groundwater',
        'USER': 'geonode',
        'PASSWORD': 'geonode',
        'HOST': 'postgres',
        'PORT': 5432,
        'CONN_MAX_AGE': 5,
        'ENGINE': 'django.contrib.gis.db.backends.postgis'}
}
