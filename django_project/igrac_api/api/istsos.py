"""Proxi API for request the url from outside API."""

import requests
from django.http import HttpResponse
from rest_framework.views import APIView

from igrac_api.authentication import APIKeyAuthentication
from igrac_api.cache import get_params


class IstsosView(APIView):
    """ISTSOS API for returning outside url."""
    authentication_classes = (APIKeyAuthentication,)

    def get(self, request):
        """GET ISTSOS API."""
        url = request.get_full_path()
        params = get_params(url)
        response = requests.get('http://istsos/istsos/istsos?' + params)
        content = response.content
        content_type = response.headers['Content-Type']
        status_code = response.status_code
        django_response = HttpResponse(
            content=content,
            status=status_code,
            content_type=content_type
        )
        return django_response
