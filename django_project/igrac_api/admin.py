from django.contrib import admin

from igrac_api.forms.api_key import CreateApiKeyForm, EditApiKeyForm
from igrac_api.models.api_key import (
    ApiKey, ApiKeyRequestLog, ApiKeyAccess
)
from igrac_api.models.isost_cache import IstsosCache, IstsosCacheQueue


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


class IstsosCacheAdmin(admin.ModelAdmin):
    list_display = ('url', 'content_type', 'generated_at')
    readonly_fields = ('url', 'cached_file', 'content_type', 'generated_at')
    actions = ['enqueue_cache_generation']

    @admin.action(description='Add selected caches to generation queue')
    def enqueue_cache_generation(self, request, queryset):
        from igrac_api.tasks.cache_istsos import run_cache_istsos
        was_idle = not IstsosCacheQueue.is_active().exists()
        for cache in queryset:
            IstsosCacheQueue.objects.create(cache=cache)
        if was_idle:
            run_cache_istsos.delay()
        self.message_user(
            request, f'{queryset.count()} cache(s) added to the queue.'
        )


class IstsosCacheQueueAdmin(admin.ModelAdmin):
    list_display = (
        'cache', 'status', 'created_at', 'started_at', 'finished_at'
    )
    list_filter = ('status',)
    readonly_fields = (
        'cache', 'status', 'created_at', 'started_at', 'finished_at', 'error'
    )
    actions = ['run_queue']

    @admin.action(description='Run selected queue entries now')
    def run_queue(self, request, queryset):
        from igrac_api.tasks.cache_istsos import run_cache_queue_istsos
        for entry in queryset:
            run_cache_queue_istsos.delay(entry.id)
        self.message_user(
            request,
            f'{queryset.count()} queue entry/entries dispatched.'
        )


admin.site.register(ApiKey, ApiKeyAdmin)
admin.site.register(ApiKeyAccess, ApiKeyAccessAdmin)
admin.site.register(ApiKeyRequestLog, ApiKeyRequestLogAdmin)
admin.site.register(IstsosCache, IstsosCacheAdmin)
admin.site.register(IstsosCacheQueue, IstsosCacheQueueAdmin)
