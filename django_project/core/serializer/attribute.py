from rest_framework import serializers
from geonode.layers.models import Attribute


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['attribute', 'description', 'attribute_label', 'attribute_type', 'visible', 'display_order']
