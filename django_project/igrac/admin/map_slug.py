from adminsortable.admin import SortableAdmin
from django.contrib import admin

from igrac.models.map_slug import MapSlugMapping


@admin.register(MapSlugMapping)
class MapSlugMappingAdmin(SortableAdmin):
    list_display = ('map', 'slug', 'featured')
    list_editable = ('featured',)
