from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from geonode.maps.views import map_view
from geonode.groups.models import GroupProfile
from geonode.monitoring import register_event
from geonode.monitoring.models import EventType
from .models.map_slug import MapSlugMapping


class HomeView(ListView):
    model = MapSlugMapping
    paginate_by = 100
    template_name = 'landing_page.html'
    context_object_name = 'maps'


def map_view_with_slug(request, slug):
    try:
        map = MapSlugMapping.objects.get(slug=slug)
    except MapSlugMapping.DoesNotExist:
        raise Http404("Map does not exist")

    return map_view(request, mapid=map.map.id)


def map_slug_metadata_detail(
        request,
        slug,
        template='maps/slug/metadata_detail_article.html'):
    try:
        map = MapSlugMapping.objects.get(slug=slug)
        map_obj = map.map
    except MapSlugMapping.DoesNotExist:
        raise Http404("Map does not exist")
    group = None
    if map_obj.group:
        try:
            group = GroupProfile.objects.get(slug=map_obj.group.name)
        except GroupProfile.DoesNotExist:
            group = None
    site_url = settings.SITEURL.rstrip('/') if settings.SITEURL.startswith('http') else settings.SITEURL
    register_event(request, EventType.EVENT_VIEW_METADATA, map_obj)
    return render(request, template, context={
        "link_online": reverse('map_view_slug', args=[slug]),
        "resource": map_obj,
        "group": group,
        'SITEURL': site_url
    })
