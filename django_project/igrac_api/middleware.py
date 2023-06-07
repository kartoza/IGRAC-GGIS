from igrac_api.models.api_key import UserApiKey


def api_keys(request):
    """SOS Api Keys"""
    if request.user.is_authenticated:
        return {
            'api_keys': list(
                UserApiKey.objects.filter(
                    user=request.user
                ).values_list('api_key', flat=True)
            )
        }
    return {}
