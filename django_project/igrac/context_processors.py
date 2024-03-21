from django.conf import settings

from igrac.models.site_preference import SitePreference
from .utilities import get_default_filter_by_group


def extra_context(request):
    """Global values to pass to templates"""
    banner_url = None
    pref = SitePreference.objects.first()
    if pref and pref.banner:
        banner_url = pref.banner.url

    defaults = dict(
        DEFAULT_GROUP_FILTER=get_default_filter_by_group(request.user),
        GOOGLE_ANALYTIC_KEY=settings.GOOGLE_ANALYTIC_KEY,
        BANNER_URL=banner_url
    )

    return defaults
