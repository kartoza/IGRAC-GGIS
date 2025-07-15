import xml.etree.ElementTree as ET

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
    organisations = ArrayField(
        models.IntegerField(),
        help_text=(
            'Organisations for this layer that '
            'will be used to filter the well data.'
        )
    )
    organisation_groups = ArrayField(
        models.IntegerField(),
        default=[],
        help_text=(
            'Organisations group for this layer that '
            'will be used to filter the well data.'
        )
    )
    additional_sql = models.TextField(
        blank=True,
        help_text=(
            'Additional sql that will be added to the sql '
            'that will be used to filter the well data.'
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
        target_layer = pref.well_and_monitoring_data_layer
        layer = self.layer
        layer.use_featureinfo_custom_template = target_layer.use_featureinfo_custom_template
        layer.featureinfo_custom_template = target_layer.featureinfo_custom_template
        layer.save()

    @property
    def all_organisations(self):
        """Return all organisations from organisations and organisation_groups.

        """
        from gwml2.models import OrganisationGroup, Organisation
        organisations = []
        if self.organisations:
            organisations += [
                f'{organisation.pk}' for organisation in
                Organisation.objects.filter(id__in=self.organisations)
            ]
        for group in OrganisationGroup.objects.filter(
                id__in=self.organisation_groups
        ):
            organisations += [
                f'{organisation.pk}' for organisation in
                group.organisations.all()
            ]
        return organisations

    @staticmethod
    def update_sql(
            tree: ET, organisations: list[int], additional_sql: str) -> ET:
        """Return sql."""
        pref = SitePreference.objects.first()
        if additional_sql:
            additional_sql = 'AND ' + additional_sql + ''
        else:
            additional_sql = ''
        data = {
            "table": 'mv_well',
            "organisations": ','.join(organisations),
            "additional_sql": additional_sql
        }
        sql = pref.well_and_monitoring_data_layer_sql.format(**data)
        tree.find('metadata/entry/virtualTable/sql').text = sql
        return tree

    def update_layer(self, organisations: list, additional_sql: str):
        """Update layer."""
        import requests
        from django.core.management import call_command

        from geonode.geoserver.helpers import gs_catalog

        layer = None
        if self.layer:
            layer = gs_catalog.get_layer(self.layer.__str__())
        if not layer:
            raise Exception(
                f'{self.layer.name} does not found. Please contact admin.'
            )

        # Fetch the xml
        workspace = layer.resource.workspace.name
        store = layer.resource.store.name
        upload_url = layer.resource.href

        # Fetch xml data
        xml_url = layer.resource.href
        xml = requests.get(
            xml_url,
            auth=(gs_catalog.username, gs_catalog.password)
        ).content

        # Update xml to new data
        tree = ET.ElementTree(ET.fromstring(xml))
        tree = GroundwaterLayer.update_sql(
            tree, organisations, additional_sql
        )

        # Change xml to string
        xml = ET.tostring(
            tree.getroot(), encoding='utf8', method='xml'
        )

        # POST data
        headers = {"content-type": "text/xml"}
        r = requests.put(
            upload_url,
            data=xml,
            auth=(gs_catalog.username, gs_catalog.password),
            headers=headers,
        )

        # Need to handle the response
        if r.status_code == 200:
            call_command('updatelayers', filter=layer.name)
            return self.layer
        else:
            raise Exception(r.content)


@receiver(post_delete, sender=GroundwaterLayer)
def groundwater_layer_deleted(
        sender, instance: GroundwaterLayer, using, **kwargs
):
    if instance.layer:
        instance.layer.delete()
