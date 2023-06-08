"""Proxi API for request the url from outside API."""

import requests
from django.http import HttpResponse
from rest_framework.views import APIView

from igrac_api.authentication import APIKeyAuthentication


class IstsosView(APIView):
    """ISTSOS API for returning outside url."""
    authentication_classes = (APIKeyAuthentication,)

    def get(self, request):
        """GET ISTSOS API."""
        params = request.get_full_path().split('?')[1]
        response = requests.get('http://istsos/istsos/istsos?' + params)

        django_response = HttpResponse(
            content=response.content,
            status=response.status_code,
            content_type=response.headers['Content-Type']
        )
        return django_response
