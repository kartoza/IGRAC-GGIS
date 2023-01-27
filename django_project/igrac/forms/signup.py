from allauth.account.forms import SignupForm
from django import forms
from django.utils.translation import gettext_lazy as _
from geonode.base.enumerations import COUNTRIES

from gwml2.models.well_management.organisation import OrganisationType


class SignupWithNameForm(SignupForm):
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=30,
        widget=forms.TextInput(
            attrs={"placeholder": _("First name")}
        )
    )
    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=150,
        widget=forms.TextInput(
            attrs={"placeholder": _("Last name")}
        )
    )

    organization = forms.CharField(
        label=_('Organization Name'),
        widget=forms.TextInput(
            attrs={"placeholder": _("Organization name")}
        )
    )
    organization_types = forms.MultipleChoiceField()
    position = forms.CharField(
        label=_('Position'),
        widget=forms.TextInput(
            attrs={"placeholder": _("Position")}
        )
    )
    city = forms.CharField(
        label=_('City'),
        widget=forms.TextInput(
            attrs={"placeholder": _("City")}
        )
    )
    area = forms.CharField(
        label=_('Administrative Area'),
        widget=forms.TextInput(
            attrs={"placeholder": _("Administrative Area")}
        )
    )
    country = forms.ChoiceField(
        label=_('Country'),
        choices=COUNTRIES
    )
    reason = forms.CharField(
        label=_('Why do you want to register in the GGIS?'),
        widget=forms.Textarea()
    )

    def __init__(self, *args, **kwargs):
        super(SignupWithNameForm, self).__init__(*args, **kwargs)
        types = [_type.name for _type in OrganisationType.objects.all()]
        self.fields['organization_types'].choices = [
            (_type.name, _type.name)
            for _type in OrganisationType.objects.all()
        ]

        # From POST data
        try:
            for _type in self.data.getlist('organization_types'):
                if _type not in types:
                    self.fields['organization_types'].choices += [
                        (_type, _type)
                    ]
        except (AttributeError, KeyError):
            pass

    def clean_organization_types(self):
        organization_types = self.cleaned_data['organization_types']
        return ', '.join(organization_types)

    def save(self, request):
        user = super().save(request)
        user.organization = self.cleaned_data.get("organization")
        user.position = self.cleaned_data.get("position")
        user.city = self.cleaned_data.get("city")
        user.area = self.cleaned_data.get("area")
        user.country = self.cleaned_data.get("country")
        user.save()
        user.igracprofile.join_reason = self.cleaned_data.get("reason")
        user.igracprofile.organization_types = self.cleaned_data.get(
            "organization_types"
        )
        user.igracprofile.save()
        return user
