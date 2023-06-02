from django.core.management.base import BaseCommand
from geonode.geoserver.helpers import gs_catalog
from geonode.layers.models import Style, Dataset
from geonode.maps.models import MapLayer


class Command(BaseCommand):
    """Clean style that does not have any relationship to dataset."""

    def handle(self, *args, **options):
        """Implementation for command.
        """
        idx = 1
        for style in Style.objects.order_by('name'):
            object_found = 0
            object_found += Dataset.objects.filter(default_style=style).count()
            object_found += Dataset.objects.filter(styles__id=style.id).count()
            object_found += MapLayer.objects.filter(
                current_style__contains=style.name
            ).count()
            gs_style = gs_catalog.get_style(
                name=style.name, workspace=style.workspace
            )
            if not object_found:
                print(f'{idx} - {style.name} - {True if gs_style else False}')
                idx += 1
                if gs_style:
                    try:
                        gs_catalog.delete(gs_style)
                    except Exception:
                        pass
                style.delete()
