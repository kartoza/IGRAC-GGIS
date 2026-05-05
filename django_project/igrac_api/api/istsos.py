"""Proxi API for request the url from outside API."""

import requests
from django.http import HttpResponse
from rest_framework.views import APIView

from igrac_api.authentication import APIKeyAuthentication
from igrac_api.cache import get_params
from igrac_api.models import IstsosCache


class IstsosView(APIView):
    """ISTSOS API for returning outside url."""
    authentication_classes = (APIKeyAuthentication,)

    def get(self, request):
        """GET ISTSOS API."""
        url = request.get_full_path()
        params = get_params(url)

        cache = IstsosCache.objects.filter(
            url__iexact=params,
            cached_file__isnull=False, generated_at__isnull=False
        ).first()
        if cache:
            return HttpResponse(
                content=cache.cached_file.read(),
                status=200,
                content_type=cache.content_type,
            )

        response = requests.get('http://istsos/istsos/istsos?' + params)
        return HttpResponse(
            content=response.content,
            status=response.status_code,
            content_type=response.headers.get('Content-Type', ''),
        )