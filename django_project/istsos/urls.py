# coding=utf-8
"""Urls for istsos apps."""

from django.conf.urls import url
from django.urls import include

from gwml2.api.authentication import TokenAuth
from gwml2.api.country import CountryAutocompleteAPI
from gwml2.api.mobile.minimized_well import (
    WellListMinimizedAPI,
    WellMeasurementListMinimizedAPI
)
from gwml2.api.mobile.well import WellCreateMinimizedAPI, WellEditMinimizedAPI
from gwml2.api.organisation import OrganisationAutocompleteAPI
from gwml2.api.task_progress import TaskProgress
from gwml2.api.upload_progress import get_progress_upload
from gwml2.api.upload_session import UploadSessionApiView
from gwml2.api.user import (UserAutocompleteAPI, UserUUIDAPI)
from gwml2.api.well_measurement import WellLevelMeasurementData
from gwml2.api.well_relation import (
    WellRelationDeleteView,
    WellRelationListView,
    WellMeasurementDataView
)
from gwml2.views.download_request import (
    DownloadRequestFormView,
    DownloadRequestDownloadNotExist,
    DownloadRequestDownloadView,
    DownloadRequestDownloadFile
)
from gwml2.views.groundwater_form import (
    WellView, WellFormView,
    WellFormCreateView
)
from gwml2.views.organisation import OrganisationFormView, OrganisationListView
from gwml2.views.plugins.measurements_chart import (
    MeasurementChart,
    MeasurementChartIframe
)
from gwml2.views.upload_session import UploadSessionDetailView
from gwml2.views.well_uploader import WellUploadView
from istsos.api.istsos import IstsosView

urlpatterns = [
    url(r'^igrac',
        view=IstsosView.as_view(),
        name='istsos-api'),
]
