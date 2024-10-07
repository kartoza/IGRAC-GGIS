from adminsortable.admin import SortableAdmin
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from preferences.admin import PreferencesAdmin

from geonode.base.admin import set_user_and_group_dataset_permission
from geonode.people.admin import ProfileAdmin
from geonode.people.models import Profile
from gwml2.models.well_management.organisation import Organisation
from igrac.forms.groundwater_layer import (
    CreateGroundwaterLayerForm, EditGroundwaterLayerForm
)
from igrac.models.groundwater_layer import GroundwaterLayer
from igrac.models.map_slug import MapSlugMapping
from igrac.models.profile import IgracProfile
from igrac.models.registration_page import RegistrationPage
from igrac.models.site_preference import SitePreference


class MapSlugMappingAdmin(SortableAdmin):
    list_display = ('map', 'slug', 'featured')
    list_editable = ('featured',)


admin.site.register(MapSlugMapping, MapSlugMappingAdmin)


class CustomPreferencesAdmin(PreferencesAdmin):
    """Custom of preferences admin."""

    readonly_fields = ('gwml2_version',)


admin.site.register(SitePreference, CustomPreferencesAdmin)

admin.site.unregister(Profile)


def make_active(modeladmin, request, queryset):
    for profile in queryset:
        profile.is_active = True
        profile.save()


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
        (_('Extended profile'), {'fields': ('organization', 'profile',
                                            'position', 'voice', 'fax',
                                            'delivery', 'city', 'area',
                                            'zipcode', 'country',
                                            'keywords')}),
        (_('IGRAC Information'),
         {'fields': ('join_reason', 'organization_types')}),
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


admin.site.register(Profile, IgracProfileAdmin)


def reassign_template(modeladmin, request, queryset):
    for layer in queryset:
        layer.assign_template()


class GroundwaterLayerAdmin(admin.ModelAdmin):
    list_display = ('layer', '_organisations', 'is_ggmn_layer')
    add_form = CreateGroundwaterLayerForm
    change_form = EditGroundwaterLayerForm

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = self.add_form
        else:
            self.form = self.change_form

        return super(GroundwaterLayerAdmin, self).get_form(
            request, obj, **kwargs
        )

    def response_post_save_change(self, request, obj: GroundwaterLayer):
        redirect_url = f'/catalogue/#/dataset/{obj.layer.pk}'
        return HttpResponseRedirect(redirect_url)

    def response_post_save_add(self, request, obj: GroundwaterLayer):
        redirect_url = f'/catalogue/#/dataset/{obj.layer.pk}'
        return HttpResponseRedirect(redirect_url)

    def _organisations(self, obj: GroundwaterLayer):
        return format_html(
            ''.join([
                f'<span style="display:inline-block; background:#ddd; margin:2px; padding: 4px 6px">{org.name}</span>'
                for org in
                Organisation.objects.filter(id__in=obj.organisations)
            ])
        )

    actions = [reassign_template]


admin.site.register(GroundwaterLayer, GroundwaterLayerAdmin)


class RegistrationPageAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'created_at', 'url')
    readonly_fields = ('code', 'user', 'created_at', 'url')

    def url(self, obj: RegistrationPage):
        """Return registration url."""
        if obj.user:
            return 'Link is not valid'
        if obj.code:
            url = reverse(
                'account_signup_with_code',
                kwargs={'code': obj.code}
            )
            return format_html(
                f'<a href="{url}" target="_blank">Registration URL</a>'
            )
        return '-'


admin.site.register(RegistrationPage, RegistrationPageAdmin)
