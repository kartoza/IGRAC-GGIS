from celery import shared_task
from celery.utils.log import get_task_logger

from igrac_api.cache import get_params
from igrac_api.models import IstsosCache, IstsosCacheQueue

logger = get_task_logger(__name__)


@shared_task(bind=True, queue='update')
def cache_istsos(self, url=None):
    """Enqueue a URL for cache generation and kick off the queue if idle.

    If no url is provided, enqueues the default GetCapabilities request.
    """
    if not url:
        url = 'http://localhost.com?service=SOS&version=1.0.0&request=GetCapabilities'
    params = get_params(url)
    cache = IstsosCache.get_or_create_for_params(params)
    was_idle = not IstsosCacheQueue.is_active().exists()
    IstsosCacheQueue.objects.create(cache=cache)
    if was_idle:
        run_cache_istsos.delay()


@shared_task(bind=True, queue='update')
def run_cache_istsos(self):
    """Process the next pending ISTSOS cache entry.

    Optionally accepts a url to enqueue before processing,
    used for manual or scheduled triggers.
    """
    IstsosCacheQueue.run()


@shared_task(bind=True, queue='update')
def run_cache_queue_istsos(self, queue_id):
    """Process the next pending ISTSOS cache entry.

    Optionally accepts a url to enqueue before processing,
    used for manual or scheduled triggers.
    """
    try:
        queue = IstsosCacheQueue.objects.get(id=queue_id)
        queue.generate()
    except IstsosCacheQueue.DoesNotExist:
        pass
