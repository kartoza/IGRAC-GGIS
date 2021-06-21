import copy
from geonode.settings import *
from wagtail.embeds.oembed_providers import youtube
from .utils import absolute_path  # noqa

INSTALLED_APPS += (
    'igrac',
    'gwml2',

    'adminsortable',

    # Wagtail
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.contrib.modeladmin',
    'wagtailmenus',
    'modelcluster',
    'preferences'
)

MIDDLEWARE = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'dj_pagination.middleware.PaginationMiddleware',
    # The setting below makes it possible to serve different languages per
    # user depending on things like headers in HTTP requests.
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'geonode.base.middleware.MaintenanceMiddleware',
    'geonode.base.middleware.ReadOnlyMiddleware',  # a Middleware enabling Read Only mode of Geonode

    # Wagtail moddleware
    'wagtail.core.middleware.SiteMiddleware',
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
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.contrib.auth.context_processors.auth',
                'geonode.context_processors.resource_urls',
                'geonode.geoserver.context_processors.geoserver_urls',
                'geonode.themes.context_processors.custom_theme',

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
TEMPLATES[0]['DIRS'] = [absolute_path('igrac', 'templates')] + TEMPLATES[0]['DIRS']

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

# gwml2 database conf
gwml2_database_conf = copy.copy(DATABASES['default'])
gwml2_database_conf['NAME'] = 'groundwater'

GWML2_DATABASE_CONFIG = 'gwml2'
DATABASES[GWML2_DATABASE_CONFIG] = gwml2_database_conf
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
