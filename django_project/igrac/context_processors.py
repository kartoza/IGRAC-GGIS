from django.conf import settings
from .utilities import get_default_filter_by_group


def extra_context(request):
    """Global values to pass to templates"""

    defaults = dict(
        DEFAULT_GROUP_FILTER=get_default_filter_by_group(request.user),
        GOOGLE_ANALYTIC_KEY=settings.GOOGLE_ANALYTIC_KEY
    )

    return defaults
