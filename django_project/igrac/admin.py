from preferences.admin import PreferencesAdmin
from adminsortable.admin import SortableAdmin
from django.contrib import admin
from .models.map_slug import MapSlugMapping
from igrac.models.site_preference import SitePreference


class MapSlugMappingAdmin(SortableAdmin):
    list_display = ('map', 'slug', 'featured')
    list_editable = ('featured',)


admin.site.register(MapSlugMapping, MapSlugMappingAdmin)
admin.site.register(SitePreference, PreferencesAdmin)
