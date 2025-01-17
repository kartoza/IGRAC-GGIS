from django.http.response import HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from core.utils import database_monitoring


class DatabaseMonitoring(APIView):
    """Return database monitoring status."""

    def get(self, request, database_name, *args):
        database_name = database_name.lower()
        try:
            database_monitoring(database_name)
            return Response()
        except Exception as e:
            return HttpResponseBadRequest(e)
