# coding=utf-8
"""Urls for istsos apps."""

from django.conf.urls import url

from igrac_api.api.istsos import IstsosView
from igrac_api.views.enrollment_form import EnrollmentFormView

urlpatterns = [
    url(r'^istsos/igrac',
        view=IstsosView.as_view(),
        name='istsos-api'),
    url(
        r'^api-enrollment/form',
        EnrollmentFormView.as_view(),
        name='api-enrollment-form'
    )
]
