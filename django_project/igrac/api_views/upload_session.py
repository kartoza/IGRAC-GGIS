from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from igrac.models.upload_session import UploadSession


class UploadSessionApiView(APIView):
    """
    Return status of the upload session
    """

    def get(self, request, token, *args):
        try:
            session = UploadSession.objects.get(
                token=token
            )
        except UploadSession.DoesNotExist:
            raise Http404('No session found')
        return Response({
            'token': session.token,
            'progress': session.progress,
            'is_processed': session.is_processed,
            'is_canceled': session.is_canceled,
            'status': session.status
        })
