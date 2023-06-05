from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField

from geonode.layers.models import Dataset


class GroundwaterLayer(models.Model):
    """GroundwaterLayer. """
    layer = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE
    )
    organisations = ArrayField(models.IntegerField())

    def __str__(self):
        return self.layer.__str__()
