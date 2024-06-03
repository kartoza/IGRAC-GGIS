from django.contrib import admin

from igrac_api.forms.api_key import CreateApiKeyForm, EditApiKeyForm
from igrac_api.models.api_key import (
    ApiKey, ApiKeyRequestLog, ApiKeyAccess
)


class ApiKeyAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'api_key', 'is_active', 'allow_write', 'max_request_per_day'
    )
    list_filter = ('user', 'is_active', 'allow_write')
    add_form = CreateApiKeyForm
    change_form = EditApiKeyForm

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = self.add_form
        else:
            self.form = self.change_form

        return super(ApiKeyAdmin, self).get_form(
            request, obj, **kwargs
        )


class ApiKeyRequestLogAdmin(admin.ModelAdmin):
    list_display = ('api_key', 'user', 'time', 'url')
    list_filter = ('api_key__api_key', 'api_key__user')

    def user(self, obj: ApiKeyRequestLog):
        return obj.api_key.user


class ApiKeyAccessAdmin(admin.ModelAdmin):
    list_display = ('api_key', 'date', 'counter')


admin.site.register(ApiKey, ApiKeyAdmin)
admin.site.register(ApiKeyAccess, ApiKeyAccessAdmin)
admin.site.register(ApiKeyRequestLog, ApiKeyRequestLogAdmin)
