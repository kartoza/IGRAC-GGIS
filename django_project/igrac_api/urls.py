# coding=utf-8
"""Urls for istsos apps."""

from django.conf.urls import url

from igrac_api.api.istsos import IstsosView

urlpatterns = [
    url(r'^istsos/igrac',
        view=IstsosView.as_view(),
        name='istsos-api')
]
