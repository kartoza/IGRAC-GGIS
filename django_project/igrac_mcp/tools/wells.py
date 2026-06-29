from asgiref.sync import sync_to_async

from gwml2.models.well import Well
from gwml2.serializer.well.well_information import GeneralInformationSerializer
from igrac_mcp.server import mcp


@mcp.tool()
async def get_wells(
    country: str = "",
    original_id: str = "",
    organisation: str = "",
    page: int = 1,
    page_size: int = 50,
) -> dict:
    """Retrieve groundwater wells from the IGRAC GGIS database.

    Returns a list of wells with general information including location,
    status, purpose, and elevation data.

    Filters (all optional, combinable):
    - country: filter by country name (case-insensitive)
    - original_id: filter by the well's original identifier (case-insensitive)
    - organisation: filter by organisation name (case-insensitive)
    - page: page number (default: 1)
    - page_size: number of results per page (default: 50, max: 200)
    """
    def _query():
        queryset = Well.objects.all()
        if country:
            queryset = queryset.filter(country__name__icontains=country)
        if original_id:
            queryset = queryset.filter(original_id__icontains=original_id)
        if organisation:
            queryset = queryset.filter(organisation__name__icontains=organisation)
        total = queryset.count()
        size = min(page_size, 200)
        offset = (page - 1) * size
        paginated = queryset[offset:offset + size]
        return {
            "total": total,
            "page": page,
            "page_size": size,
            "results": list(GeneralInformationSerializer(paginated, many=True).data),
        }

    return await sync_to_async(_query)()
