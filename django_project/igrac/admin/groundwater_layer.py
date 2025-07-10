from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.html import format_html

from gwml2.models.well_management.organisation import Organisation
from igrac.forms.groundwater_layer import (
    CreateGroundwaterLayerForm, EditGroundwaterLayerForm
)
from igrac.models.groundwater_layer import GroundwaterLayer


def reassign_template(modeladmin, request, queryset):
    for layer in queryset:
        layer.assign_template()


@admin.register(GroundwaterLayer)
class GroundwaterLayerAdmin(admin.ModelAdmin):
    list_display = ('layer', '_organisations')
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
