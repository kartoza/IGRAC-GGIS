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
from igrac.g3p import (
    G3PTimeseriesData, 
    G3PTimeseriesChart,
    G3PTimeseriesChartIframe
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
    url(r'^api/G3P_data/', G3PTimeseriesData.as_view(), name='G3P_data'),
    url(r'^g3p/(?P<name>[\w\+%_& ]+)/(?P<id>[^/]+)/chart/iframe',
        G3PTimeseriesChartIframe.as_view(),
        name='g3p-timeseries-chart-iframe'),
    url(r'^g3p/(?P<name>[^/]+)/(?P<id>[^/]+)/chart',
        G3PTimeseriesChart.as_view(),
        name='g3p-timeseries-chart'),
    url(r'^g3p/(?P<name>[^/]+)/(?P<ylabel>[^/]+)/(?P<xlabel>[^/]+)/(?P<id>[^/]+)/chart',
        G3PTimeseriesChart.as_view(),
        name='g3p-timeseries-chart'),
]
