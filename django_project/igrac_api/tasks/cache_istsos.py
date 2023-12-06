import os

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings

from igrac_api.cache import generate_cache

folder = os.path.join(settings.GWML2_FOLDER, 'istsos')

logger = get_task_logger(__name__)


@shared_task(bind=True, queue='update')
def cache_istsos(self, url=None):
    """Cache istsos."""
    if url:
        generate_cache(url)
    else:
        generate_cache(
            '/istsos?service=SOS&version=1.0.0&request=getcapabilities',
            delete_folder=True
        )
