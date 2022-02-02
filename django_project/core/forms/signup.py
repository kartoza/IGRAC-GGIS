from django import forms
from django.utils.translation import gettext_lazy as _
from allauth.account.forms import SignupForm


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

    def save(self, request):
        user = super().save(request)
        user.organization = self.cleaned_data.get("organization")
        user.save()
        return user
