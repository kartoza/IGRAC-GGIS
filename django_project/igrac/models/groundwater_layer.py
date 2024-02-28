from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_delete
from django.dispatch import receiver

from geonode.layers.models import Dataset
from igrac.models.site_preference import SitePreference


class GroundwaterLayer(models.Model):
    """GroundwaterLayer. """
    layer = models.OneToOneField(
        Dataset,
        on_delete=models.CASCADE
    )
    organisations = ArrayField(models.IntegerField())

    def __str__(self):
        return self.layer.__str__()

    class Meta:
        verbose_name = 'Well and monitoring data layer'
        verbose_name_plural = 'Well and monitoring data layers'

    def assign_template(self, target_layer=None):
        """Assign template."""
        pref = SitePreference.objects.first()
        if not target_layer:
            target_layer = pref.ggmn_layer
        layer = self.layer
        layer.use_featureinfo_custom_template = target_layer.use_featureinfo_custom_template
        layer.featureinfo_custom_template = target_layer.featureinfo_custom_template
        layer.save()


@receiver(post_delete, sender=GroundwaterLayer)
def groundwater_layer_deleted(
        sender, instance: GroundwaterLayer, using, **kwargs
):
    if instance.layer:
        instance.layer.delete()
