# coding=utf-8
from django.contrib.contenttypes.models import ContentType

from geonode.documents.models import Document
from geonode.groups.models import GroupProfile
from geonode.layers.models import Dataset
from geonode.maps.models import Map

STOP_WORDS = (
    'a', 'an', 'and', 'if', 'is', 'the', 'in', 'i', 'you', 'other',
    'this', 'that', 'to',
)


def check_slug(queryset, slug):
    """
    This function checks slug within a model queryset
    and return a new incremented slug when there are duplicates.

    """

    registered_slug = queryset.values_list('slug', flat=True)
    new_slug = slug
    if slug in registered_slug:
        match_slug = [s for s in registered_slug if slug in s]
        num = len(match_slug)
        num_char = 50 - (len(str(num)) + 1)
        new_slug = slug[:num_char] + '-' + str(num)

    return new_slug


def get_default_filter_by_group(user):
    """
    Set layer/map/document filter by user's group by default
    """
    groups = GroupProfile.objects.filter(
        group__in=user.groups.exclude(name='anonymous')
    ).values_list('slug', flat=True)

    filter = ""
    for group in groups:
        filter = filter + "&" + "group__group_profile__slug__in=" + group

    return filter


def get_related_documents(resource):
    if isinstance(resource, Dataset) or isinstance(resource, Map):
        content_type = ContentType.objects.get_for_model(resource)
        return Document.objects.filter(
            links__content_type=content_type,
            links__object_id=resource.pk
        )
    else:
        return None
