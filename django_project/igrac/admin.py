from preferences.admin import PreferencesAdmin
from django.contrib import admin
from .models.map_slug import MapSlugMapping
from igrac.models.site_preference import SitePreference
from igrac.models.upload_session import UploadSession


class MapSlugMappingAdmin(admin.ModelAdmin):
    list_display = ('map', 'slug')


class UploadSessionAdmin(admin.ModelAdmin):
    list_display = (
        'uploader',
        'uploaded_at',
        'category',
        'is_processed',
        'is_canceled'
    )
    list_filter = (
        'category',
        'is_processed',
        'is_canceled'
    )


admin.site.register(MapSlugMapping, MapSlugMappingAdmin)
admin.site.register(SitePreference, PreferencesAdmin)
admin.site.register(UploadSession, UploadSessionAdmin)
