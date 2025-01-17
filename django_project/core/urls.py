from geonode.urls import *
from core.api.layer import LayerAttributeAPI
from core.api.database_monitoring import DatabaseMonitoring

geonode_additional_api = [
    url(r'^api/layer/(?P<alternate>[\w\+%_&: ]+)/attributes',
        view=LayerAttributeAPI.as_view(),
        name='geonode_layer_attribute'),
    url(r'^api/database_monitoring/(?P<database_name>[\w\+%_&: ]+)',
        view=DatabaseMonitoring.as_view(),
        name='database_monitoring'),
]
urlpatterns = [
                  url(r'^', include('igrac.urls')),
                  url(r'^', include('igrac_api.urls')),
              ] + urlpatterns + geonode_additional_api

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
