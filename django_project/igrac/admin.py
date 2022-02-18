from preferences.admin import PreferencesAdmin
from adminsortable.admin import SortableAdmin
from django.contrib import admin

from geonode.base.admin import set_user_and_group_layer_permission
from geonode.people.admin import ProfileAdmin
from geonode.people.models import Profile
from igrac.models.map_slug import MapSlugMapping
from igrac.models.site_preference import SitePreference


class MapSlugMappingAdmin(SortableAdmin):
    list_display = ('map', 'slug', 'featured')
    list_editable = ('featured',)


admin.site.register(MapSlugMapping, MapSlugMappingAdmin)
admin.site.register(SitePreference, PreferencesAdmin)

admin.site.unregister(Profile)


def make_active(modeladmin, request, queryset):
    for profile in queryset:
        profile.is_active = True
        profile.save()


class IgracProfileAdmin(ProfileAdmin):
    actions = [set_user_and_group_layer_permission, make_active]


admin.site.register(Profile, IgracProfileAdmin)
