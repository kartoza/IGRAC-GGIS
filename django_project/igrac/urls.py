# coding=utf-8
"""Urls for igrac apps."""

from django.conf.urls import url
from django.urls import include
from igrac.views import HomeView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls


urlpatterns = [
    url(r'^$',
        view=HomeView.as_view(),
        name='home_igrac'),
    url(r'^groundwater/', include('gwml2.urls')),
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^pages/', include(wagtail_urls)),
]
