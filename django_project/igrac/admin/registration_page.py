from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from igrac.models.registration_page import RegistrationPage


@admin.register(RegistrationPage)
class RegistrationPageAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'created_at', 'url')
    readonly_fields = ('code', 'user', 'created_at', 'url')

    def url(self, obj: RegistrationPage):
        """Return registration url."""
        if obj.user:
            return 'Link is not valid'
        if obj.code:
            url = reverse(
                'account_signup_with_code',
                kwargs={'code': obj.code}
            )
            return format_html(
                f'<a href="{url}" target="_blank">Registration URL</a>'
            )
        return '-'
