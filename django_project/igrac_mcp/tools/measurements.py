from typing import Literal

from asgiref.sync import sync_to_async

from gwml2.models.well import (
    Well,
    WellLevelMeasurement,
    WellQualityMeasurement,
    WellYieldMeasurement,
)
from gwml2.serializer.well.measurement import (
    WellLevelMeasurementSerializer,
    WellQualityMeasurementSerializer,
    WellYieldMeasurementSerializer,
)
from igrac_mcp.server import mcp

MEASUREMENT_TYPES = {
    'level': (WellLevelMeasurement, WellLevelMeasurementSerializer, 'welllevelmeasurement_set'),
    'quality': (WellQualityMeasurement, WellQualityMeasurementSerializer, 'wellqualitymeasurement_set'),
    'yield': (WellYieldMeasurement, WellYieldMeasurementSerializer, 'wellyieldmeasurement_set'),
}


@mcp.tool()
async def get_well_measurements(
    original_id: str,
    measurement_type: Literal['level', 'quality', 'yield'] = 'level',
    time_start: str = "",
    time_end: str = "",
    value_min: float = None,
    value_max: float = None,
    page: int = 1,
    page_size: int = 50,
) -> dict:
    """Retrieve measurements for a specific groundwater well.

    Returns time-series measurement data including value, parameter,
    time, and methodology.

    Args:
    - original_id: the well's original identifier (required)
    - measurement_type: type of measurement to retrieve — 'level' (default), 'quality', or 'yield'
    - time_start: filter measurements from this datetime (ISO format, e.g. '2024-01-01' or '2024-01-01T00:00:00')
    - time_end: filter measurements up to this datetime (ISO format)
    - value_min: filter measurements with value >= this number
    - value_max: filter measurements with value <= this number
    - page: page number (default: 1)
    - page_size: number of results per page (default: 50, max: 200)
    """
    def _query():
        try:
            well = Well.objects.get(original_id=original_id)
        except Well.DoesNotExist:
            return {"total": 0, "page": page, "page_size": page_size, "results": []}

        _, serializer_class, related_name = MEASUREMENT_TYPES[measurement_type]
        queryset = getattr(well, related_name).all()
        if time_start:
            queryset = queryset.filter(time__gte=time_start)
        if time_end:
            queryset = queryset.filter(time__lte=time_end)
        if value_min is not None:
            queryset = queryset.filter(value__value__gte=value_min)
        if value_max is not None:
            queryset = queryset.filter(value__value__lte=value_max)
        total = queryset.count()
        size = min(page_size, 200)
        offset = (page - 1) * size
        paginated = queryset[offset:offset + size]
        return {
            "total": total,
            "page": page,
            "page_size": size,
            "results": list(serializer_class(paginated, many=True).data),
        }

    return await sync_to_async(_query)()
