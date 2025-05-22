# coding=utf-8
"""Urls for istsos apps."""

from django.urls import re_path

from igrac_api.api.istsos import IstsosView

urlpatterns = [
    re_path(
        r'^istsos$',
        view=IstsosView.as_view(),
        name='istsos-api'
    )
]
