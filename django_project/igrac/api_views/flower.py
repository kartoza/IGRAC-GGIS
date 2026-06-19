"""Proxy view for Flower (Celery monitoring UI). Admin-only."""

import requests
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
class FlowerProxyView(View):
    """Reverse proxy to the internal Flower service (Celery monitoring UI).

    Flower runs inside the Docker network without an exposed port. This view
    forwards every HTTP request — including task revoke/terminate POSTs — to
    http://flower:5555/flower/<path> and streams the response back to the
    browser.

    Access is restricted to Django staff/admin users via staff_member_required.
    CSRF is exempted because Flower manages its own form tokens; authentication
    is enforced at the Django layer before any request reaches Flower.

    URL: /flower/<path>
    """

    def dispatch(self, request, path='', *args, **kwargs):
        flower_internal_url = settings.FLOWER_INTERNAL_URL
        url = f'{flower_internal_url}/flower/{path}'
        qs = request.META.get('QUERY_STRING', '')
        if qs:
            url += '?' + qs

        headers = {
            key[5:].replace('_', '-').title(): val
            for key, val in request.META.items()
            if key.startswith('HTTP_')
        }

        resp = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=request.body,
            allow_redirects=False,
            timeout=30,
        )

        return HttpResponse(
            content=resp.content,
            status=resp.status_code,
            content_type=resp.headers.get('Content-Type', ''),
        )
