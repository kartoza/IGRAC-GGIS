from rest_framework.serializers import ModelSerializer

from igrac_api.models.api_key import UserApiKey


class UserApiKeySerializer(ModelSerializer):
    """Serializer for UserApiKey."""

    class Meta:
        model = UserApiKey
        exclude = ()
