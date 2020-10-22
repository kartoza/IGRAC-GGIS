from preferences.admin import PreferencesAdmin
from django.contrib import admin
from .models.map_slug import MapSlugMapping
from igrac.models.site_preference import SitePreference


class MapSlugMappingAdmin(admin.ModelAdmin):
    list_display = ('map', 'slug')


admin.site.register(MapSlugMapping, MapSlugMappingAdmin)
admin.site.register(SitePreference, PreferencesAdmin)
