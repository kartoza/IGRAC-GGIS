from geonode.urls import *
from igrac.views import map_view_with_slug

urlpatterns = [
                  url(r'^', include('igrac.urls')),
              ] + urlpatterns + [
                  url(r'^(?P<slug>[^/]+)$',
                      view=map_view_with_slug,
                      name='map_view_slug'),
              ]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
