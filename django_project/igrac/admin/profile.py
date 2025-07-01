from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from geonode.base.admin import set_user_and_group_dataset_permission
from geonode.people.admin import ProfileAdmin
from geonode.people.models import Profile
from igrac.models.profile import IgracProfile

admin.site.unregister(Profile)


def make_active(modeladmin, request, queryset):
    for profile in queryset:
        profile.is_active = True
        profile.save()


@admin.register(Profile)
class IgracProfileAdmin(ProfileAdmin):
    list_display = (
        'id', 'username', 'email', 'first_name', 'last_name',
        'is_staff', 'is_active', 'organization', 'position', 'join_reason'
    )
    search_fields = (
        'username', 'organization', 'profile',
        'first_name', 'last_name', 'email'
    )
    actions = [set_user_and_group_dataset_permission, make_active]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (
            _('Extended profile'),
            {
                'fields': (
                    'organization', 'profile', 'position', 'voice', 'fax',
                    'delivery', 'city', 'area', 'zipcode', 'country',
                    'keywords'
                )
            }
        ),
        (
            _('IGRAC Information'),
            {'fields': ('join_reason', 'organization_types')}
        ),
    )
    readonly_fields = ('join_reason', 'organization_types')

    def join_reason(self, obj: Profile):
        try:
            return obj.igracprofile.join_reason
        except IgracProfile.DoesNotExist:
            return ''

    def organization_types(self, obj: Profile):
        try:
            return obj.igracprofile.organization_types
        except IgracProfile.DoesNotExist:
            return ''
