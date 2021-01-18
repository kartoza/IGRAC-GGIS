from geonode.urls import *
from core.api.layer import LayerAttributeAPI

geonode_additional_api = [
    url(r'^layer/(?P<alternate>[\w\+%_&: ]+)/attributes',
        view=LayerAttributeAPI.as_view(),
        name='geonode_layer_attribute'),
]
urlpatterns = [
                  url(r'^', include('igrac.urls')),
                  url(r'^api/', include(geonode_additional_api)),
              ] + urlpatterns

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
