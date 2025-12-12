from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView

from geonode.layers.models import Dataset
from geonode.maps.models import Map
from gwml2.serializer.organisation_contributor import (
    OrganisationContributorSerializer, Organisation
)
from igrac.models.groundwater_layer import GroundwaterLayer


class GroundwaterResourceContributorPage(APIView):
    """Return the contributor page content of a groundwater page."""

    def get(self, request, id, resource_type, *args):
        """Get page content of a geonode page."""
        if resource_type not in ['map', 'dataset']:
            return HttpResponseBadRequest(f'{resource_type} not recognized')

        # Get resource object
        if resource_type == 'map':
            resource = get_object_or_404(Map, pk=id)
            dataset_ids = [
                layer.dataset for layer in resource.maplayers.all()
            ]

        else:
            dataset_ids = [get_object_or_404(Dataset, pk=id).id]

        if not dataset_ids:
            return HttpResponseBadRequest(
                f'No contributors found for {resource_type} {id}'
            )

        organisations = []
        for layer in GroundwaterLayer.objects.filter(layer__in=dataset_ids):
            organisations += layer.all_organisations

        if not organisations:
            return HttpResponseBadRequest(
                f'No contributors found for {resource_type} {id}'
            )

        # Render the contributor page template with organisations
        return render(
            request,
            'igrac/contributor_page.html',
            {
                'organisations': OrganisationContributorSerializer(
                    Organisation.objects.filter(id__in=organisations).filter(
                        active=True).order_by('name'),
                    many=True
                ).data,
            }
        )
