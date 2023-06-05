import xml.etree.ElementTree as ET

import requests
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.core.management import call_command
from geoserver.support import build_url

from geonode.geoserver.helpers import gs_catalog
from geonode.layers.models import Dataset
from gwml2.models.download_request import WELL_AND_MONITORING_DATA, GGMN
from gwml2.models.well_management.organisation import Organisation
from igrac.models.groundwater_layer import GroundwaterLayer
from igrac.models.site_preference import SitePreference

User = get_user_model()


# TODO:
#  All hardcoded need to be saved on the preferences

class _BaseGroundwaterLayerForm(forms.ModelForm):
    layer = None
    well_type = forms.ChoiceField(
        choices=(
            (WELL_AND_MONITORING_DATA, WELL_AND_MONITORING_DATA),
            (GGMN, GGMN)
        )
    )
    selected_orgs = forms.ModelMultipleChoiceField(
        Organisation.objects.all(),
        label='Organisations',
        widget=FilteredSelectMultiple('organisations', False),
        help_text=(
            'Organisation that will used to filter the data. '
        )
    )

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        if self.instance and self.instance.organisations:
            self.fields['selected_orgs'].initial = Organisation.objects.filter(
                id__in=self.instance.organisations)

    class Meta:
        model = GroundwaterLayer
        exclude = ('layer', 'organisations')

    def clean(self):
        cleaned_data = self.cleaned_data
        organisations = cleaned_data['selected_orgs']
        cleaned_data['organisations'] = organisations

        try:
            dataset = self.run()
            cleaned_data['layer'] = dataset
        except Exception as e:
            raise forms.ValidationError(f'{e}')
        return cleaned_data

    def save(self, commit=True):
        instance = super(_BaseGroundwaterLayerForm, self).save(commit)
        cleaned_data = self.cleaned_data
        instance.organisations = list(
            cleaned_data['organisations'].values_list('pk', flat=True)
        )
        instance.layer = cleaned_data['layer']
        instance.save()
        return instance

    def update_sql(self, tree):
        """Return sql."""
        organisations = [
            f'{organisation.pk}' for organisation in
            self.cleaned_data['organisations']
        ]
        well_type = self.cleaned_data['well_type']
        mv = None
        if well_type == WELL_AND_MONITORING_DATA:
            mv = 'mv_well'
        elif well_type == GGMN:
            mv = 'mv_well_ggmn'
        sql = (
                "select id, ggis_uid, original_id, name, feature_type,purpose, status,organisation, country, year_of_drilling, aquifer_name, aquifer_type,manager, detail, location, created_at, created_by, last_edited_at, last_edited_by "
                f"from {mv} where organisation_id IN (" +
                f"{','.join(organisations)}" +
                ") order by created_at DESC"
        )
        tree.find('metadata/entry/virtualTable/sql').text = sql

    def run(self):
        """Run it for duplication data."""
        name = self.cleaned_data['name']
        target_layer_name = name.replace(' ', '_')

        # Fetch the xml
        layer = self.layer
        workspace = layer.resource.workspace.name
        store = layer.resource.store.name
        upload_url = build_url(
            gs_catalog.service_url,
            ["workspaces", workspace, "datastores", store, "featuretypes"]
        )

        # Fetch xml data
        xml_url = layer.resource.href
        xml = requests.get(xml_url).content

        # Update xml to new data
        tree = ET.ElementTree(ET.fromstring(xml))
        tree.find('name').text = target_layer_name
        tree.find('nativeName').text = target_layer_name
        tree.find(
            'metadata/entry/virtualTable/name').text = target_layer_name
        tree.find('title').text = name

        self.update_sql(tree)

        # Change xml to sting
        xml = ET.tostring(
            tree.getroot(), encoding='utf8', method='xml'
        )

        # POST data
        headers = {"content-type": "text/xml"}
        r = requests.post(
            upload_url,
            data=xml,
            auth=(gs_catalog.username, gs_catalog.password),
            headers=headers,
        )

        # Need to handle the response
        if r.status_code == 201:
            layer = gs_catalog.get_layer(f'{workspace}:{target_layer_name}')
            style = gs_catalog.get_style(
                'Groundwater_Well', workspace='groundwater'
            )
            if style:
                layer.default_style = style
                gs_catalog.save(layer)
            call_command('updatelayers', filter=target_layer_name)
            try:
                dataset = Dataset.objects.get(
                    workspace=workspace, store=store, name=target_layer_name
                )
                return dataset
            except Dataset.DoesNotExist:
                return None
        else:
            raise Exception(r.content)


class CreateGroundwaterLayerForm(_BaseGroundwaterLayerForm):
    """Create groundwater layer."""
    name = forms.CharField(
        help_text='The layer name that will be created.',
        widget=forms.TextInput(attrs={'style': 'width:500px'})
    )

    def clean_well_type(self):
        """Well type."""
        well_type = self.cleaned_data['well_type']
        pref = SitePreference.objects.first()
        target_layer = None
        if well_type == WELL_AND_MONITORING_DATA:
            target_layer = pref.well_and_monitoring_data_layer.__str__()
        elif well_type == GGMN:
            target_layer = pref.ggmn_layer.__str__()

        # Check target layer on geoserver
        self.layer = None
        if target_layer:
            self.layer = gs_catalog.get_layer(target_layer)
        if not self.layer:
            raise forms.ValidationError(
                f'{target_layer} does not found. Please contact admin.'
            )
        return well_type

    def clean_name(self):
        """Validate name."""
        name = self.cleaned_data['name']
        layer = self.layer
        if layer:
            workspace = layer.resource.workspace.name
            target_layer_name = name.replace(' ', '_')
            layer_name = f'{workspace}:{target_layer_name}'
            layer = gs_catalog.get_layer(layer_name)
            if layer:
                raise forms.ValidationError(
                    f'Layer with this name is already exist'
                )
        else:
            raise forms.ValidationError(
                f'Can not proceed, layer does not found'
            )
        return name

    class Meta:
        model = GroundwaterLayer
        exclude = ('layer', 'organisations')


class EditGroundwaterLayerForm(_BaseGroundwaterLayerForm):
    """Edit groundwater layer."""
    layer = None
    well_type = forms.ChoiceField(
        choices=(
            (WELL_AND_MONITORING_DATA, WELL_AND_MONITORING_DATA),
            (GGMN, GGMN)
        )
    )
    selected_orgs = forms.ModelMultipleChoiceField(
        Organisation.objects.all(),
        label='Organisations',
        widget=FilteredSelectMultiple('organisations', False),
        help_text=(
            'Organisation that will used to filter the data. '
        )
    )

    class Meta:
        model = GroundwaterLayer
        exclude = ('layer', 'organisations', 'name')

    def run(self):
        """Run it for duplication data."""
        layer = None
        if self.instance.layer:
            layer = gs_catalog.get_layer(self.instance.layer.__str__())
        if not layer:
            raise Exception(
                f'{self.instance.layer.name} does not found. Please contact admin.'
            )

        # Fetch the xml
        workspace = layer.resource.workspace.name
        store = layer.resource.store.name
        upload_url = layer.resource.href

        # Fetch xml data
        xml_url = layer.resource.href
        xml = requests.get(xml_url).content

        # Update xml to new data
        tree = ET.ElementTree(ET.fromstring(xml))
        self.update_sql(tree)

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
            return self.instance.layer
        else:
            raise Exception(r.content)
