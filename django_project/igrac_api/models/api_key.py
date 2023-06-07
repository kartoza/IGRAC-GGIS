import binascii
import os

from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.utils import timezone

User = get_user_model()


class ApiKey(models.Model):
    """
    This model provide user API KEY to access API of istsos
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    api_key = models.CharField(
        max_length=40, primary_key=True
    )
    is_active = models.BooleanField(
        default=True
    )
    allow_write = models.BooleanField(
        default=False,
        help_text='Allow this api key to write data.'
    )
    max_request_per_day = models.IntegerField(
        help_text=(
            'Max request per day for the api key. '
            'Keep blank or null for unlimited.'
        ),
        null=True, blank=True
    )

    @property
    def limit(self):
        """Return limit of request."""
        return self.max_request_per_day

    @staticmethod
    def generate_key():
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.api_key

    @staticmethod
    def get_user_from_api_key(api_key):
        """ return user from API Key

        :param api_key: user that going to be checked
        :type api_key: User

        :return: User found or None
        :rtype: User
        """
        try:
            return ApiKey.objects.get(
                api_key=api_key,
                is_active=True
            ).user
        except ApiKey.DoesNotExist:
            return None

    @staticmethod
    def get_key_from_api_key(api_key):
        """ return user from API Key

        :param api_key: user that going to be checked
        :type api_key: User

        :return: ApiKey
        :rtype: ApiKey
        """
        try:
            return ApiKey.objects.get(
                api_key=api_key
            )
        except ApiKey.DoesNotExist:
            return None


class ApiKeyAccess(models.Model):
    """API Key Access."""

    api_key = models.ForeignKey(ApiKey, on_delete=models.CASCADE)
    date = models.DateField()
    counter = models.IntegerField(default=0)

    @staticmethod
    def request(api_key: ApiKey, url: str, method: str):
        """Doing a request."""
        now = timezone.now()
        date = now.date()
        access, _ = ApiKeyAccess.objects.get_or_create(
            api_key=api_key, date=date
        )
        access.counter += 1
        if api_key.limit is not None and access.counter > api_key.limit:
            return False

        access.save()
        ApiKeyRequestLog.objects.create(
            api_key=api_key, time=now, url=url, method=method
        )
        return True


class ApiKeyRequestLog(models.Model):
    """API Key for request log."""

    api_key = models.ForeignKey(ApiKey, on_delete=models.CASCADE)
    method = models.CharField(max_length=126)
    time = models.DateTimeField()
    url = models.TextField()
