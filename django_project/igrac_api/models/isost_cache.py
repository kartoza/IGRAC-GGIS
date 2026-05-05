import requests
from django.contrib.gis.db import models
from django.core.files.base import ContentFile
from django.utils import timezone


class IstsosCache(models.Model):
    """Cache for ISTSOS API responses."""

    url = models.TextField(unique=True)
    cached_file = models.FileField(upload_to='istsos/', null=True, blank=True)
    content_type = models.CharField(max_length=256, blank=True, default='')
    generated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.url

    def generate(self):
        """Fetch from upstream ISTSOS and save response to cached_file."""
        response = requests.get('http://istsos/istsos/istsos?' + self.url)
        if response.status_code == 200:
            filename = self.url.replace('/', '-')
            if self.cached_file:
                self.cached_file.delete(save=False)
            self.cached_file.save(
                filename, ContentFile(response.content), save=False
            )
            self.content_type = response.headers.get('Content-Type', '')
            self.generated_at = timezone.now()
            self.save(
                update_fields=['cached_file', 'content_type', 'generated_at']
            )

    @classmethod
    def get_or_create_for_params(cls, params: str) -> 'IstsosCache':
        """Return the cache entry for the given params string, creating it if absent."""
        cache, _ = cls.objects.get_or_create(url=params)
        return cache


class IstsosCacheQueue(models.Model):
    """Queue for tracking IstsosCache generation jobs."""

    STATUS_PENDING = 'pending'
    STATUS_RUNNING = 'running'
    STATUS_DONE = 'done'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_RUNNING, 'Running'),
        (STATUS_DONE, 'Done'),
        (STATUS_FAILED, 'Failed'),
    ]

    cache = models.ForeignKey(
        IstsosCache, on_delete=models.CASCADE, related_name='queue_entries'
    )
    status = models.CharField(
        max_length=16, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.cache.url} [{self.status}]'

    @staticmethod
    def is_active():
        return IstsosCacheQueue.objects.exclude(
            status__in=[
                IstsosCacheQueue.STATUS_FAILED,
                IstsosCacheQueue.STATUS_DONE
            ]
        )

    @staticmethod
    def run():
        """Run the cache generation and update status accordingly."""
        is_active = IstsosCacheQueue.is_active().order_by('created_at').first()
        if is_active and is_active.status == IstsosCacheQueue.STATUS_PENDING:
            is_active.generate()

    def generate(self):
        """Run the cache generation and update status accordingly.

        Guards against a duplicate task by atomically claiming the pending slot;
        exits early if another worker already started this entry.
        """
        self.status = self.STATUS_RUNNING
        self.started_at = timezone.now()
        self.save(update_fields=['status', 'started_at'])
        try:
            self.cache.generate()
            self.status = self.STATUS_DONE
        except Exception as e:
            self.status = self.STATUS_FAILED
            self.error = str(e)
        finally:
            self.finished_at = timezone.now()
            self.save(update_fields=['status', 'error', 'finished_at'])
            from igrac_api.tasks.cache_istsos import run_cache_istsos
            run_cache_istsos.delay()
