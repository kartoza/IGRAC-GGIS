from importlib.metadata import version, PackageNotFoundError

from django.db import models
from preferences.models import Preferences

from core.middleware import (
    gwml2_version, igrac_version, geonode_version, igrac_commit
)
from geonode.layers.models import Dataset
from gwml2.utils.template_check import compare_ods_xlsx_template


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
    well_and_monitoring_data_layer_sql = models.TextField(
        default="""
                select id,
                       ggis_uid,
                       original_id,
                       name,
                       feature_type,
                       purpose,
                       status,
                       organisation,

                       number_of_measurements_level   as "groundwater_level_data",
                       number_of_measurements_quality as "groundwater_quality_data",
                       number_of_measurements_yield   as "abstraction_discharge",

                       country,
                       year_of_drilling,
                       aquifer_name,
                       aquifer_type,
                       manager,
                       detail,
                       location,
                       created_at,
                       created_by,
                       last_edited_at,
                       last_edited_by,

                       first_time_measurement         as first_recorded_measurement,
                       last_time_measurement          as last_recorded_measurement,
                       is_groundwater_level           as groundwater_level,
                       is_groundwater_quality         as groundwater_quality,
                       ground_surface_elevation,
                       ground_surface_elevation_unit,
                       dem_elevation,
                       dem_elevation_unit
                from {table}
                where organisation_id IN ({organisations}) {additional_sql}
                order by created_at DESC
                """
    )
    download_readme_text = models.TextField(
        blank=True,
        null=True,
        help_text='Readme text to be included in the download zip file.'
    )
    banner = models.ImageField(
        upload_to='images',
        null=True, blank=True,
    )

    # Legacy
    legacy_ggmn_download_readme_text = models.TextField(
        blank=True,
        null=True,
        help_text='Readme text to be included in the download zip file of GGMN data type.'
    )

    @property
    def geonode_version(self):
        """Return the Geonode version."""
        return geonode_version()

    @property
    def geonode_mapstore_client_version(self):
        """Return the Geonode mapstore client version."""
        try:
            return version("django-geonode-mapstore-client")
        except PackageNotFoundError:
            return "Not installed"

    @property
    def igrac_version(self):
        """Return the IGRAC version."""
        return igrac_version()

    @property
    def igrac_commit(self):
        """Return the IGRAC commit."""
        return igrac_commit()

    @property
    def gwml2_version(self):
        """Return the GWML2 version."""
        return gwml2_version()

    @property
    def wells_sync(self):
        """Return if wells synced."""
        return compare_ods_xlsx_template(
            'wells.xlsx', 'General Information'
        )

    @property
    def monitoring_data_sync(self):
        """Return if monitoring_data synced."""
        return compare_ods_xlsx_template(
            'monitoring_data.xlsx', 'Monitoring data'
        )

    @property
    def drilling_and_construction_sync(self):
        """Return if drilling_and_construction synced."""
        return compare_ods_xlsx_template(
            'drilling_and_construction.xlsx',
            'drilling and construction'
        )
