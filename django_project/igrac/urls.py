# coding=utf-8
"""Urls for igrac apps."""

from django.conf.urls import url
from django.urls import include
from .views import HomeView, map_view_with_slug

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from igrac.views import (
    MapSlugMetadataDetail, MapMetadataDetail, CustomSignupView
)

urlpatterns = [
    url(r'^$',
        view=HomeView.as_view(),
        name='home_igrac'),
    url(r'^view/(?P<id>[^/]+)/metadata_detail/article$',
        MapSlugMetadataDetail.as_view(),
        name='map_view_slug_metadata_detail'),
    url(r'^maps/(?P<id>[^/]+)/metadata_detail/article$',
        MapMetadataDetail.as_view(),
        name='map_view_metadata_detail'),
    url(r'^view/(?P<slug>[^/]+)$',
        view=map_view_with_slug,
        name='map_view_slug'),
    url(r'^groundwater/', include('gwml2.urls')),
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^wagtail/documents/', include(wagtaildocs_urls)),
    url(r'^about/', include(wagtail_urls)),
    url(
        r'^account/signup/',
        CustomSignupView.as_view(),
        name='account_signup'
    ),
]
