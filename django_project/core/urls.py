"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from geonode.urls import urlpatterns as geonode_urlpatterns


# GeoNode has to be in root url conf.
# It cannot be included in include() function because it contains i18n urls
urlpatterns = [
    url(r'^', include('igrac.urls')),
]

for geonode_pattern in geonode_urlpatterns:
    try:
        if 'admin' in geonode_pattern.app_dict:
            geonode_urlpatterns.remove(geonode_pattern)
    except AttributeError:
        continue

urlpatterns += geonode_urlpatterns

urlpatterns += [
    url('^admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
