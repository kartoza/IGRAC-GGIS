# coding=utf-8
"""Urls for igrac apps."""

from django.urls import re_path, include
from django.views.generic import TemplateView
from wagtail.admin.urls import urlpatterns as wagtailadmin_urls
from wagtail.documents.urls import urlpatterns as wagtaildocs_urls
from wagtail.urls import urlpatterns as wagtail_urls

from igrac.api_views.featured import FeaturedMaps
from igrac.g3p import (
    G3PTimeseriesData,
    G3PTimeseriesChart,
    G3PTimeseriesChartIframe
)
from igrac.views import (
    MapSlugMetadataDetail, MapMetadataDetail, CustomSignupView
)
from .views import map_view_with_slug

urlpatterns = [
    re_path(
        r'^view/(?P<id>[^/]+)/metadata_detail/article$',
        MapSlugMetadataDetail.as_view(),
        name='map_view_slug_metadata_detail'
    ),
    re_path(
        r'^maps/(?P<id>[^/]+)/metadata_detail/article$',
        MapMetadataDetail.as_view(),
        name='map_view_metadata_detail'
    ),
    re_path(
        r'^view/(?P<slug>[^/]+)/$',
        view=map_view_with_slug,
        name='map_view_slug'
    ),
    re_path(
        r'^igrac_api/featured/$',
        view=FeaturedMaps.as_view(),
        name='featured_maps'
    ),
    re_path(
        r'^/api/v2/maps/$',
        view=FeaturedMaps.as_view(),
        name='featured_maps'
    ),
    re_path(r'^groundwater/', include('gwml2.urls')),
    re_path(r'^cms/', include(wagtailadmin_urls)),
    re_path(r'^wagtail/documents/', include(wagtaildocs_urls)),
    re_path(r'^about/', include(wagtail_urls)),
    re_path(
        r'^account/signup/not-found',
        TemplateView.as_view(template_name='account/signup-not-found.html'),
        name='account_signup_not_found'
    ),
    re_path(
        r'^account/signup/not-valid',
        TemplateView.as_view(template_name='account/signup-not-valid.html'),
        name='account_signup_not_valid'
    ),
    re_path(
        r'^account/signup/(?P<code>[^/]+)/',
        CustomSignupView.as_view(),
        name='account_signup_with_code'
    ),
    re_path(
        r'^account/signup/',
        CustomSignupView.as_view(),
        name='account_signup'
    ),
    re_path(
        r'^api/G3P_data/',
        G3PTimeseriesData.as_view(),
        name='G3P_data'
    ),
    re_path(
        r'^g3p/(?P<name>[\w\+%_& ]+)/(?P<id>[^/]+)/chart/iframe',
        G3PTimeseriesChartIframe.as_view(),
        name='g3p-timeseries-chart-iframe'
    ),
    re_path(
        r'^g3p/(?P<name>[^/]+)/(?P<id>[^/]+)/chart',
        G3PTimeseriesChart.as_view(),
        name='g3p-timeseries-chart'
    ),
    re_path(
        r'^g3p/(?P<name>[^/]+)/(?P<ylabel>[^/]+)/(?P<xlabel>[^/]+)/(?P<id>[^/]+)/chart',
        G3PTimeseriesChart.as_view(),
        name='g3p-timeseries-chart'
    ),
]
