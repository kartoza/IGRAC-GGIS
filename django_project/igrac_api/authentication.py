__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '28/01/19'

from rest_framework import authentication, exceptions

from igrac_api.models.api_key import UserApiKey, ApiKeyAccess


class APIKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        api_key = request.GET.get('api-key', None)
        if not api_key:
            raise exceptions.AuthenticationFailed('api-key is needed')
        key = UserApiKey.get_key_from_api_key(api_key)
        if not key:
            raise exceptions.AuthenticationFailed(
                'API key invalid. '
                'Please recreate your key using the enrollment form.'
            )
        if not key.is_active:
            raise exceptions.AuthenticationFailed(
                'This API key is not active. '
                'Please wait for it to be approved by the admins.'
            )
        user = key.user
        if not user:
            raise exceptions.AuthenticationFailed('api-key is invalid')
        if request.method != 'GET' and not key.allow_write:
            raise exceptions.AuthenticationFailed(
                'This API key does not include access permissions to post data. '
                'Please ask the admins if you need POST permissions.'
            )
        allow = ApiKeyAccess.request(
            key, request.build_absolute_uri(), request.method
        )
        if not allow:
            raise exceptions.AuthenticationFailed(
                "The number of today API requests is too high. "
                f"The limit is {key.limit} per day. "
                "Please ask admin to increase the limit. "
            )

        return (user, None)
