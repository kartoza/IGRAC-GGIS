from django.db import models
from preferences.models import Preferences

from core.middleware import gwml2_version, igrac_version, geonode_version
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
    well_and_monitoring_data_layer_sql = models.TextField(
        default="""
            select 
                id, ggis_uid, original_id, name, feature_type,purpose, 
                status, organisation,
                 
                number_of_measurements_level as "groundwater_level_data", 
                number_of_measurements_quality as "groundwater_quality_data", 
                number_of_measurements_yield as "abstraction_discharge",
                
                country, year_of_drilling, aquifer_name, aquifer_type,manager, 
                detail, location, 
                created_at, created_by, last_edited_at, last_edited_by,
                
                first_time_measurement,
                last_time_measurement,
                is_groundwater_level,
                is_groundwater_quality 
             from {table} 
             where organisation_id IN ({organisations}) 
             order by created_at DESC        
        """
    )
    download_readme_text = models.TextField(
        blank=True,
        null=True,
        help_text='Readme text to be included in the download zip file.'
    )
    ggmn_download_readme_text = models.TextField(
        blank=True,
        null=True,
        help_text='Readme text to be included in the download zip file of GGMN data type.'
    )
    banner = models.ImageField(
        upload_to='images',
        null=True, blank=True,
    )

    @property
    def geonode_version(self):
        """Return the Geonode version."""
        return geonode_version()

    @property
    def igrac_version(self):
        """Return the IGRAC version."""
        return igrac_version()

    @property
    def gwml2_version(self):
        """Return the GWML2 version."""
        return gwml2_version()
