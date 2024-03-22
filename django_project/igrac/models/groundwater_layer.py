from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_delete, post_save
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
    is_ggmn_layer = models.BooleanField(
        default=False,
        help_text=(
            'Indicate that this layer is ggmn layer. '
            'It will be used to construct the data to be downloaded.'
        )
    )

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


@receiver(post_save, sender=GroundwaterLayer)
def groundwater_layer_saved(
        sender, instance: GroundwaterLayer, using, **kwargs
):
    from gwml2.tasks.data_file_cache.country_recache import (
        generate_data_all_country_cache
    )
    from gwml2.tasks.data_file_cache.organisation_cache import (
        generate_data_all_organisation_cache
    )
    if instance.is_ggmn_layer:
        generate_data_all_country_cache.delay()
        generate_data_all_organisation_cache.delay()
