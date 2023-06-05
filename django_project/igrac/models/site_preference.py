from django.db import models
from preferences.models import Preferences

from geonode.layers.models import Dataset


class SitePreference(Preferences):
    """Model to define site preferences."""

    manual_page_link = models.CharField(
        blank=True,
        max_length=100,
        help_text='Link to manual page'
    )
    well_and_monitoring_data_layer = models.OneToOneField(
        Dataset,
        null=True, blank=True,
        related_name='preference_well_and_monitoring_data_layer',
        on_delete=models.SET_NULL
    )
    ggmn_layer = models.OneToOneField(
        Dataset,
        null=True, blank=True,
        related_name='preference_ggmn_layer',
        on_delete=models.SET_NULL
    )
