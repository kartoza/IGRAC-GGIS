from allauth.account.forms import SignupForm
from django import forms
from django.utils.translation import gettext_lazy as _
from geonode.base.enumerations import COUNTRIES


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
    position = forms.CharField(
        label=_('Position'),
        widget=forms.TextInput(
            attrs={"placeholder": _("position")}
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

    def save(self, request):
        user = super().save(request)
        user.organization = self.cleaned_data.get("organization")
        user.position = self.cleaned_data.get("position")
        user.city = self.cleaned_data.get("city")
        user.area = self.cleaned_data.get("area")
        user.country = self.cleaned_data.get("country")
        user.save()
        user.igracprofile.join_reason = self.cleaned_data.get("reason")
        user.igracprofile.save()
        return user
