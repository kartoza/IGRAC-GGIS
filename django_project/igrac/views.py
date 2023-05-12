from django.conf import settings
from django.http import Http404
from django.views.generic import ListView, TemplateView

from allauth.account.views import SignupView

from geonode.maps.models import Map
from geonode.maps.views import map_embed
from geonode.groups.models import GroupProfile
from geonode.base import register_event
from geonode.monitoring.models import EventType
from geonode.documents.models import get_related_documents

from igrac.models.map_slug import MapSlugMapping
from igrac.forms.signup import SignupWithNameForm


class CustomSignupView(SignupView):
    form_class = SignupWithNameForm

    def get_context_data(self, **kwargs):
        ret = super(CustomSignupView, self).get_context_data(**kwargs)
        ret.update({'account_geonode_local_signup': settings.SOCIALACCOUNT_WITH_GEONODE_LOCAL_SINGUP})
        return ret


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

    return map_embed(request, mapid=map.map.id)


class MetadataDetail(TemplateView):
    """ View for returning template that showing map metadata"""
    template_name = 'maps/metadata_detail_article.html'

    def get_map_object(self, id):
        """ Return map object from id
        """
        raise NotImplementedError

    def get_context_data(self, **kwargs):
        context = super(MetadataDetail, self).get_context_data(**kwargs)
        id = kwargs['id']
        map = self.get_map_object(id)
        group = None
        if map.group:
            try:
                group = GroupProfile.objects.get(slug=map.group.name)
            except GroupProfile.DoesNotExist:
                group = None
        site_url = settings.SITEURL.rstrip('/') if settings.SITEURL.startswith('http') else settings.SITEURL
        register_event(self.request, EventType.EVENT_VIEW_METADATA, map)
        context.update({
            "resource": map,
            "group": group,
            'SITEURL': site_url,
            "documents": get_related_documents(map)
        })
        return context


class MapSlugMetadataDetail(MetadataDetail):
    def get_map_object(self, id):
        """ Return map object from id
        """
        try:
            map = MapSlugMapping.objects.get(slug=id)
            return map.map
        except MapSlugMapping.DoesNotExist:
            raise Http404("Map does not exist")


class MapMetadataDetail(MetadataDetail):
    def get_map_object(self, id):
        """ Return map object from id
        """
        try:
            return Map.objects.get(id=id)
        except MapSlugMapping.DoesNotExist:
            raise Http404("Map does not exist")
