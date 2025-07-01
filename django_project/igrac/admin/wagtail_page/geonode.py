from adminsortable.admin import SortableAdmin
from django.contrib import admin
from django.utils.html import format_html

from igrac.models import GeonodePage


@admin.register(GeonodePage)
class GeonodePageAdmin(SortableAdmin):
    list_display = ('title', 'slug', '_datasets', '_maps')
    filter_horizontal = ('maps', 'datasets')

    def _datasets(self, obj: GeonodePage):
        return format_html(
            ''.join([
                f'<span style="display:inline-block; background:#ddd; margin:2px; padding: 4px 6px">{resource.title}</span>'
                for resource in obj.datasets.all()
            ])
        )

    def _maps(self, obj: GeonodePage):
        return format_html(
            ''.join([
                f'<span style="display:inline-block; background:#ddd; margin:2px; padding: 4px 6px">{resource.title}</span>'
                for resource in obj.maps.all()
            ])
        )
