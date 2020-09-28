import json
from django.db import models
from django.contrib.postgres.fields import JSONField
from preferences.models import Preferences


class SitePreference(Preferences):
    """Model to define site preferences."""

    manual_page_link = models.CharField(
        blank=True,
        max_length=100,
        help_text='Link to manual page'
    )
