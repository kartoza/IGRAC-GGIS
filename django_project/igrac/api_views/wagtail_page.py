from django.core.exceptions import FieldError
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from wagtail.rich_text import expand_db_html

from igrac.models.wagtail_page.geonode import GeonodePage


def return_edit_link(user, page: GeonodePage):
    """Return edit link for this page."""
    if user.is_superuser:
        return (
            '<div style="display: flex; justify-content: right; opacity: 0.5;">'
            f'<a href="/cms/pages/{page.id}/edit/" target="_blank">Edit content</a>'
            "</div>"
        )
    return ""


class PageContent(APIView):
    """Return page content of a geonode page."""

    def get(self, request, id, *args):
        """Get page content of a geonode page."""
        page = get_object_or_404(GeonodePage, id=id)
        return HttpResponse(
            expand_db_html(page.body) + return_edit_link(user=request.user, page=page),
            content_type="text/html",
        )


class GeonodeBaseResourcePageContent(APIView):
    """Return base resource page content of a geonode page."""

    def get_body(self, id, resource_type):
        """Return combined CMS body HTML for a geonode resource.

        Returns None if no CMS page is linked to the resource.
        Raises FieldError if resource_type is not a valid relation.
        """
        if resource_type == "geostory":
            resource_type = "geostorie"

        filter_kwargs = {f"{resource_type}s__id": id}
        pages = GeonodePage.objects.filter(**filter_kwargs)
        if not pages.exists():
            return None
        htmls = []
        for page in pages:
            htmls.append(
                expand_db_html(page.body) + return_edit_link(user=self.request.user, page=page)
            )
        return "<hr/>".join(htmls)

    def get(self, request, id, resource_type, *args):
        """Get page content of a geonode page."""
        try:
            body = self.get_body(id, resource_type)
            if body is None:
                raise Http404()
            return HttpResponse(body, content_type="text/html")
        except FieldError:
            return HttpResponseBadRequest(f"{resource_type} not found")
