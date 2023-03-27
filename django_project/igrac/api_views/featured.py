from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from geonode.maps.models import Map
from geonode.base.api.serializers import ResourceBaseSerializer
from geonode.base.models import (
    Link,
    ResourceBase,
)
from igrac.models.map_slug import MapSlugMapping


class FeaturedSerializer(ResourceBaseSerializer):

    slug = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()

    def get_slug(self, obj: ResourceBase):
        map_slug = MapSlugMapping.objects.filter(map=obj).first()
        if map_slug:
            return map_slug.slug
        return ''

    def get_detail_url(self, obj: ResourceBase):
        map_slug = MapSlugMapping.objects.filter(map=obj).first()
        if map_slug:
            return map_slug.slug
        return ''

    class Meta:
        model = ResourceBase
        name = ResourceBaseSerializer.Meta.name
        view_name = ResourceBaseSerializer.Meta.view_name
        fields = ResourceBaseSerializer.Meta.fields + ('slug',)


class FeaturedMaps(APIView):
    def get(self, request, *args):
        featured_map = Map.objects.filter(
            featured=True
        ).order_by(
            'mapslugmapping__order', 'id'
        )
        serializer = FeaturedSerializer(
            featured_map,
            many=True
        )
        return Response({
            "links": {
                "next": None,
                "previous": None
            },
            "total": featured_map.count(),
            "page": 1,
            "page_size": 99,
            "resources": serializer.data
        })
