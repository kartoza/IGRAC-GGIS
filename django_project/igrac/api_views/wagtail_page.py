from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from igrac.models.wagtail_page.geonode import GeonodePage


class PageContent(APIView):
    """Return page content of a geonode page."""

    def get(self, request, id, *args):
        """Get page content of a geonode page."""
        page = get_object_or_404(GeonodePage, id=id)
        return page.body_only_view(request)
