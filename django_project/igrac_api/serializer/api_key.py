from rest_framework.serializers import ModelSerializer

from igrac_api.models.api_key import ApiKey


class ApiKeySerializer(ModelSerializer):
    """Serializer for ApiKey."""

    class Meta:
        model = ApiKey
        exclude = ()
