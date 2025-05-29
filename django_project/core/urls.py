from core.api.database_monitoring import DatabaseMonitoring
from core.api.layer import LayerAttributeAPI
from geonode.urls import *

geonode_additional_api = [
    re_path(
        r'^api/layer/(?P<alternate>[\w\+%_&: ]+)/attributes',
        view=LayerAttributeAPI.as_view(),
        name='geonode_layer_attribute'
    ),
    re_path(
        r'^api/database_monitoring/(?P<database_name>[\w\+%_&: ]+)',
        view=DatabaseMonitoring.as_view(),
        name='database_monitoring'
    ),
]

urlpatterns = [
                  re_path(r'^', include('igrac.urls')),
                  re_path(r'^', include('igrac_api.urls')),
              ] + urlpatterns + geonode_additional_api

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
