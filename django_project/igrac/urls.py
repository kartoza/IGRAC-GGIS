# coding=utf-8
"""Urls for igrac apps."""

from django.conf.urls import url
from django.urls import include
from .views import HomeView, map_view_with_slug
from igrac.api_views.upload_session import UploadSessionApiView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls


urlpatterns = [
    url(r'^$',
        view=HomeView.as_view(),
        name='home_igrac'),
    url(r'^view/(?P<slug>[^/]+)$',
        view=map_view_with_slug,
        name='map_view_slug'),
    url(r'^groundwater/', include('gwml2.urls')),
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^wagtail/documents/', include(wagtaildocs_urls)),
    url(r'^pages/', include(wagtail_urls)),
    url(r'^upload-session/'
        r'(?P<token>\b[0-9a-f]{8}\b-[0-9a-f]{4}-'
        r'[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b)/',
        view=UploadSessionApiView.as_view(),
        name='upload_session_progress'),
]
