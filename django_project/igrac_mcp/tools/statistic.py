from asgiref.sync import sync_to_async
from rest_framework.test import APIRequestFactory

from gwml2.api.statistic import (
    CountryStatisticAPI,
    OrganisationStatisticAPI,
    QualityControlStatisticAPI,
)
from igrac_mcp.server import mcp

factory = APIRequestFactory()


@mcp.tool()
async def get_organisation_statistic() -> dict:
    """Retrieve well/spring statistics per organisation from the gwml2 statistic API.

    Use this to quickly check the total number of wells or measurements
    across the whole database (or per organisation) without paginating
    through get_wells / get_well_measurements.

    Response shape:
    - count: number of active organisations
    - count_well: total wells across ALL organisations (global well count)
    - count_spring: total springs across all organisations
    - count_well_with_level: wells that have at least one level measurement
    - count_well_with_quality: wells that have at least one quality measurement
    - organisations: list of per-organisation records, each with:
        - id, name, country_id
        - is_ggmn: whether the organisation belongs to the GGMN group
        - data_is_from_api: whether data is harvested from an external API
        - data_date_start, data_date_end: date range of the organisation's data
        - data_stats: dict with count_well, count_spring,
          count_well_with_level, count_well_with_quality for this
          organisation only
        - metadata_cache_generated_at: when data_stats was last computed
    """
    def _fetch():
        request = factory.get('/')
        response = OrganisationStatisticAPI.as_view()(request)
        return response.data

    return await sync_to_async(_fetch)()


@mcp.tool()
async def get_country_statistic() -> dict:
    """Retrieve well statistics per country from the gwml2 statistic API.

    Use this to check well/measurement counts broken down by country
    without paginating through get_wells / get_well_measurements.

    Response shape:
    - count: number of countries that have data
    - countries: list of per-country records, each with:
        - id, name
        - statistic_observations_repository: cached stats (same shape as
          below) for wells belonging to Groundwater Observations
          Repository organisations in this country, or null if none
        - statistic_ggmn: cached stats for wells belonging to GGMN
          organisations in this country, or null if none

      Each cached stats dict (statistic_observations_repository /
      statistic_ggmn) contains:
        - data_date_start, data_date_end: date range of measurements
        - count_well: number of wells
        - count_well_with_level: wells with at least one level measurement
        - count_well_with_quality: wells with at least one quality measurement
        - count_spring: number of springs
        - count_measurement: total measurements (level + quality + yield)
        - count_measurement_level, count_measurement_quality,
          count_measurement_yield: measurement counts by type
    """
    def _fetch():
        request = factory.get('/')
        response = CountryStatisticAPI.as_view()(request)
        return response.data

    return await sync_to_async(_fetch)()


@mcp.tool()
async def get_quality_control_statistic(
    data_type: str = "",
    country_ids: list[int] = None,
) -> dict:
    """Retrieve quality-control flag statistics from the gwml2 statistic API.

    Use this to check how many wells have quality-control issues (and how
    many are clean) without paginating through get_wells /
    get_well_measurements. Counts are over wells (not measurement rows).

    Args:
    - data_type: filter by data source — 'GGMN' or
      'Groundwater Observations Repository' (default: all)
    - country_ids: optional list of country IDs to filter by

    Response shape:
    - groundwater_level_time_gap_num: wells flagged for a time gap in
      groundwater level measurements
    - groundwater_level_value_gap_num: wells flagged for a value gap in
      groundwater level measurements
    - groundwater_level_strange_value_num: wells flagged for a strange/
      outlier groundwater level value
    - no_flag: wells with no quality-control flag (includes wells that
      have no quality-control record at all)
    """
    def _fetch():
        payload = {}
        if data_type:
            payload["data_type"] = data_type
        if country_ids:
            payload["country_ids"] = country_ids
        request = factory.post('/', payload, format='json')
        response = QualityControlStatisticAPI.as_view()(request)
        return response.data

    return await sync_to_async(_fetch)()