from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.html import format_html

from gwml2.models.well_management.organisation import (
    Organisation, OrganisationGroup
)
from igrac.forms.groundwater_layer import (
    CreateGroundwaterLayerForm, EditGroundwaterLayerForm
)
from igrac.models.groundwater_layer import GroundwaterLayer


def reassign_template(modeladmin, request, queryset):
    for layer in queryset:
        layer.assign_template()


@admin.register(GroundwaterLayer)
class GroundwaterLayerAdmin(admin.ModelAdmin):
    list_display = (
        'layer', '_organisations', '_organisation_groups', 'additional_sql'
    )
    add_form = CreateGroundwaterLayerForm
    change_form = EditGroundwaterLayerForm

    def get_fieldsets(self, request, obj=None):
        """Return fieldsets."""
        if obj is None:
            return (
                (
                    '',
                    {
                        'fields': (
                            'name', 'selected_orgs', 'selected_org_group',
                            'additional_sql'
                        ),
                    }
                ),
            )
        else:
            return (
                (
                    '',
                    {
                        'fields': (
                            'selected_orgs', 'selected_org_group',
                            'additional_sql'
                        ),
                    }
                ),
            )

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

    def _organisation_groups(self, obj: GroundwaterLayer):
        return format_html(
            ''.join([
                f'<span style="display:inline-block; background:#ddd; margin:2px; padding: 4px 6px">{org.name}</span>'
                for org in
                OrganisationGroup.objects.filter(
                    id__in=obj.organisation_groups
                )
            ])
        )

    actions = [reassign_template]
