from django import forms
from django.contrib.auth import get_user_model

from igrac_api.models.api_key import ApiKey

User = get_user_model()


class CreateApiKeyForm(forms.ModelForm):
    """Form to create Api Key."""

    class Meta:
        model = ApiKey
        exclude = ('api_key',)

    def save(self, commit=True):
        """Save form."""
        instance = super(CreateApiKeyForm, self).save(commit)
        instance.api_key = ApiKey.generate_key()
        instance.save()
        return instance


class EditApiKeyForm(forms.ModelForm):
    """Form to create Api Key."""

    class Meta:
        model = ApiKey
        exclude = ()
