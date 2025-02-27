from allauth.account.views import SignupView
from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView

from geonode.base import register_event
from geonode.groups.models import GroupProfile
from geonode.maps.models import Map
from geonode.maps.views import map_embed
from geonode.monitoring.models import EventType
from igrac.forms.signup import SignupWithNameForm
from igrac.models.map_slug import MapSlugMapping
from igrac.models.registration_page import RegistrationPage
from igrac.utilities import get_related_documents


class RegistrationNotFound(Exception):
    pass


class RegistrationNotValid(Exception):
    pass


class CustomSignupView(SignupView):
    form_class = SignupWithNameForm

    def registration_page(self):
        """Return registration page."""
        try:
            registration_page = RegistrationPage.objects.get(
                code=self.kwargs.get('code', ''))
            if registration_page.user:
                raise RegistrationNotValid()
        except RegistrationPage.DoesNotExist:
            raise RegistrationNotFound()
        return registration_page

    def get(self, request, *args, **kwargs):
        """GET File."""
        try:
            self.registration_page()
        except RegistrationNotFound:
            return redirect('account_signup_not_found')
        except RegistrationNotValid:
            return redirect('account_signup_not_valid')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ret = super(CustomSignupView, self).get_context_data(**kwargs)
        ret.update(
            {
                'account_geonode_local_signup':
                    settings.SOCIALACCOUNT_WITH_GEONODE_LOCAL_SINGUP
            }
        )
        return ret

    def get_success_url(self):
        """We save the user to Registration page."""
        try:
            registration_page = self.registration_page()
            registration_page.user = self.user
            registration_page.save()
        except (AttributeError, RegistrationNotFound, RegistrationNotValid):
            pass
        return super(CustomSignupView, self).get_success_url()


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
        site_url = settings.SITEURL.rstrip('/') if settings.SITEURL.startswith(
            'http') else settings.SITEURL
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
