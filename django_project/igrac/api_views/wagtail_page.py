from django.core.exceptions import FieldError
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from wagtail.rich_text import expand_db_html

from igrac.models.wagtail_page.geonode import GeonodePage


class PageContent(APIView):
    """Return page content of a geonode page."""

    def get(self, request, id, *args):
        """Get page content of a geonode page."""
        page = get_object_or_404(GeonodePage, id=id)
        return page.body_only_view(request)


class GeonodeBaseResourcePageContent(APIView):
    """Return base resource page content of a geonode page."""

    @staticmethod
    def get_body(id, resource_type):
        """Return combined CMS body HTML for a geonode resource.

        Returns None if no CMS page is linked to the resource.
        Raises FieldError if resource_type is not a valid relation.
        """
        if resource_type == 'geostory':
            resource_type = 'geostorie'

        filter_kwargs = {f"{resource_type}s__id": id}
        pages = GeonodePage.objects.filter(**filter_kwargs)
        if not pages.exists():
            return None
        return '<hr/>'.join(
            [expand_db_html(page.body) for page in pages]
        )

    def get(self, request, id, resource_type, *args):
        """Get page content of a geonode page."""
        try:
            body = self.get_body(id, resource_type)
            if body is None:
                raise Http404()
            return HttpResponse(body, content_type='text/html')
        except FieldError:
            return HttpResponseBadRequest(f'{resource_type} not found')
