import copy

from celery.schedules import crontab
from wagtail.embeds.oembed_providers import youtube

from geonode.settings import *
from .utils import absolute_path  # noqa

if 'mapstore2_adapter.geoapps.dashboards' in INSTALLED_APPS:
    INSTALLED_APPS = list(INSTALLED_APPS)
    INSTALLED_APPS.remove('mapstore2_adapter.geoapps.dashboards')
    INSTALLED_APPS = tuple(INSTALLED_APPS)

INSTALLED_APPS += (
    'igrac',
    'gwml2',
    'igrac_api',

    'adminsortable',

    # Wagtail
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.modeladmin',
    'wagtail.sites',
    'wagtail.embeds',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',
    'wagtailmenus',
    "wagtailautocomplete",
    'modelcluster',
    'preferences'
)

MIDDLEWARE += (
    # Wagtail moddleware
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
TEMPLATES = [
    {
        'NAME': 'GeoNode Project Templates',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': CONTEXT_PROCESSORS + [
                # IGRAC context processor
                'igrac.context_processors.extra_context',

                # WAGTAIL
                'wagtail.contrib.settings.context_processors.settings',
                'wagtailmenus.context_processors.wagtailmenus',

                # Preferences
                'preferences.context_processors.preferences_cp',

                # igrac specified
                'core.middleware.project_version',
            ],
            'debug': DEBUG,
        },
    },
]

# Additional locations of static files
STATICFILES_DIRS = [absolute_path('igrac', 'static'), ] + STATICFILES_DIRS

# Additional locations of templates
TEMPLATES[0]['DIRS'] = [absolute_path('igrac', 'templates')] + TEMPLATES[0][
    'DIRS']

# Wagtail Settings
WAGTAIL_SITE_NAME = 'My Example Site'
WAGTAILMENUS_SITE_SPECIFIC_TEMPLATE_DIRS = True
WAGTAILEMBEDS_RESPONSIVE_HTML = True
youtube_https = youtube.copy()
youtube_https['endpoint'] = "https://www.youtube.com/oembed"
WAGTAILEMBEDS_FINDERS = [
    {
        'class': 'wagtail.embeds.finders.oembed',
        'providers': [youtube_https],
        'options': {'scheme': 'https'}
    },
    {
        'class': 'wagtail.embeds.finders.oembed',
    }
]
# -- END Settings for Wagtail

# -- gwml2 database conf
gwml2_database_conf = copy.copy(DATABASES['default'])
gwml2_database_conf['NAME'] = 'groundwater'
GWML2_DATABASE_CONFIG = 'gwml2'

GROUNDWATER_DATABASE_URL = os.getenv("GROUNDWATER_DATABASE_URL", None)
if GROUNDWATER_DATABASE_URL:
    _db_conf = dj_database_url.parse(
        GROUNDWATER_DATABASE_URL, conn_max_age=GEONODE_DB_CONN_MAX_AGE
    )
    gwml2_database_conf.update(_db_conf)
DATABASES[GWML2_DATABASE_CONFIG] = gwml2_database_conf
# --

DATABASE_ROUTERS = ['gwml2.router.GWML2Router']
ROOT_URLCONF = 'core.urls'

LOCALE_PATHS += (
    os.path.join(PROJECT_ROOT, 'igrac', 'locale'),
    os.path.join(PROJECT_ROOT, 'gwml2', 'locale'),
)

CSRF_COOKIE_HTTPONLY = False
RESOURCE_PUBLISHING = False
FREETEXT_KEYWORDS_READONLY = True

UPLOADER['SUPPORTED_CRS'].append('ESRI:54030')
EPSG_CODE_MATCHES['ESRI:54030'] = '(54030) World_Robinson'

# Where the file uploaded temporary saved
FILE_UPLOAD_TEMP_DIR = os.getenv('FILE_UPLOAD_TEMP_DIR', None)

GOOGLE_ANALYTIC_KEY = os.getenv('GOOGLE_ANALYTIC_KEY', None)

if MAPSTORE_BASELAYERS:
    MAPSTORE_BASELAYERS.insert(len(MAPSTORE_BASELAYERS) - 1, {
        "type": "tileprovider",
        "title": "CartoDB - Positron",
        "name": "CartoDB - Positron",
        "provider": "CartoDB.Positron",
        "source": "CartoDB",
        "group": "background",
        "thumbURL": "%sstatic/img/positron.png" % SITEURL,
        "visibility": False
    })

if 'gwml2' in INSTALLED_APPS:
    CELERY_BEAT_SCHEDULE['generate_downloadable_file_cache'] = {
        'task': 'gwml2.tasks.well.generate_downloadable_file_cache',
        'schedule': crontab(minute=0, hour=0, day_of_week=6)
    }
    CELERY_BEAT_SCHEDULE['run_all_harvester'] = {
        'task': 'gwml2.tasks.harvester.run_all_harvester',
        'schedule': crontab(minute=0, hour='*/3'),
    }
    CELERY_BEAT_SCHEDULE['clean_download_file'] = {
        'task': 'gwml2.tasks.clean.clean_download_file',
        'schedule': crontab(hour='*/1'),
    }
    CELERY_BEAT_SCHEDULE['resume_all_uploader'] = {
        'task': 'gwml2.tasks.upload_session.resume_all_uploader',
        'schedule': crontab(minute='*/5'),
    }

GWML2_FOLDER = os.getenv(
    'GWML_FOLDER', os.path.join(PROJECT_ROOT, 'gwml2-file')
)
MEASUREMENTS_FOLDER = os.path.join(
    GWML2_FOLDER, os.getenv('MEASUREMENTS_FOLDER', 'measurements')
)
SFTP_FOLDER = os.getenv(
    'SFTP_FOLDER', os.path.join(PROJECT_ROOT, 'sftp')
)

MANAGEMENT_COMMANDS_EXPOSED_OVER_HTTP = set(
    [
        "ping_mngmt_commands_http",
        "updatelayers",
        "sync_geonode_datasets",
        "sync_geonode_maps",
        "importlayers",
        "set_all_datasets_metadata",
        "set_layers_permissions",
        "refresh_materialized_views",
        "generate_data_countries_cache",
        "generate_data_organisations_cache",
        "generate_data_wells_cache",
        "generate_well_measurement_cache",
        "generate_uploader_report",
    ]
    + ast.literal_eval(
        os.getenv("MANAGEMENT_COMMANDS_EXPOSED_OVER_HTTP ", "[]"))
)
