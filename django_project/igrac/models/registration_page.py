"""Registration page that needs to be used for register."""

import random
import string
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


def id_generator(
        size=36,
        chars=string.ascii_letters + string.digits + '+_-'
):
    """ID Generator."""
    return ''.join(random.choice(chars) for _ in range(size))


class RegistrationPage(models.Model):
    """Registration page that has random uuid.

    User can just register through this model.
    When user is created through this page, it will be invalid
    and need to create new one.
    """

    user = models.OneToOneField(
        User, on_delete=models.SET_NULL,
        blank=True, null=True
    )
    code = models.TextField(max_length=16, unique=True)
    created_at = models.DateTimeField(
        _('Requested at'),
        default=datetime.now, blank=True
    )
    note = models.TextField(
        blank=True, null=True
    )

    def __str__(self):
        return str(self.code)

    def save(self, *args, **kwargs):
        """Save model."""
        if not self.code:
            self.code = id_generator()
        return super().save(*args, **kwargs)
