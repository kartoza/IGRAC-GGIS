from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from geonode.layers.models import Dataset
from core.serializer.attribute import AttributeSerializer


class LayerAttributeAPI(APIView):
    permission_classes = []
    """
    Return status of the upload session
    """

    def get(self, request, alternate, *args):
        try:
            dataset = Dataset.objects.get(alternate=alternate)
            return Response(AttributeSerializer(
                dataset.attribute_set.all(), many=True).data)
        except Dataset.DoesNotExist:
            raise Http404('Layer not found')
