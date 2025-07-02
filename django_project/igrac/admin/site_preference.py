from django.contrib import admin
from preferences.admin import PreferencesAdmin

from igrac.models.site_preference import SitePreference


@admin.register(SitePreference)
class CustomPreferencesAdmin(PreferencesAdmin):
    """Custom of preferences admin."""

    readonly_fields = (
        'geonode_version', 'geonode_mapstore_client_version',
        'igrac_version', 'igrac_commit', 'gwml2_version',

    )
