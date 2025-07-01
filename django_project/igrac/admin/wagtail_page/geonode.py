from adminsortable.admin import SortableAdmin
from django.contrib import admin

from igrac.models import GeonodePage


@admin.register(GeonodePage)
class GeonodePageAdmin(SortableAdmin):
    list_display = ('title', 'slug')
    filter_horizontal = ('maps', 'datasets')
