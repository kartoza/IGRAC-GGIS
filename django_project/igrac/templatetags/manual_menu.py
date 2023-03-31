from django import template
from django.utils.safestring import mark_safe
from geonode.base.models import Configuration
from geonode_mapstore_client.templatetags.get_menu_json import get_user_menu
register = template.Library()


def get_list_element(list_data, active_slug):
    element = '<ul>'
    for data in list_data:
        if data['url']:
            element += '<li {c}><a href="{url}" >{title} {indicator}</a>'.format(
                url=data['url'],
                title=data['title'],
                indicator='(Pending)' if not data['live'] else '',
                c="data-jstree='{\"opened\":true,\"selected\":true}'" if data['slug'] == active_slug else ''
            )
        if 'children' in data:
            element += get_list_element(data['children'], active_slug)
        element += '</li>'
    element += '</ul>'
    return element


@register.simple_tag(name='manual_menu')
def manual_menu(menu_data, active_slug):
    """Returns side menu for manual page"""
    element = get_list_element(menu_data, active_slug)
    return mark_safe(element)


@register.simple_tag(name='explore_map')
def explore_map(maps):
    """Returns side menu for map menu"""
    output = []
    for _map in maps:
        # skip if not featured
        if not _map.featured:
            continue

        # replace thumbnail_url with curated_thumbs
        if hasattr(_map.map, 'curatedthumbnail'):
            if hasattr(_map.map.curatedthumbnail.img_thumbnail, 'url'):
                _map.map.thumbnail_url = _map.map.curatedthumbnail.thumbnail_url
        output.append(_map)
    return output


def _is_mobile_device(context):
    if context and 'request' in context:
        req = context['request']
        return req.user_agent.is_mobile
    return False

def _is_logged_in(context):
    if context and 'request' in context:
        req = context['request']
        return req.user.is_authenticated
    return False

@register.simple_tag(
    takes_context=True, name='get_igrac_base_left_topbar_menu')
def get_igrac_base_left_topbar_menu(context):

    is_mobile = _is_mobile_device(context)
    is_logged_in = _is_logged_in(context)

    user = context.get('request').user
    users = {
        "label": "Users",
        "type": "dropdown",
        "items": [
            {
                "type": "link",
                "href": "/people/",
                "label": "People"
            },
            {
                "type": "link",
                "href": "/groups/",
                "label": "Groups"
            },
            {
                "type": "link",
                "href": "/groundwater/organisation/",
                "label": "Organisations"
            } if user.is_superuser else None,
        ]
    }
    if user.is_authenticated and not Configuration.load().read_only:
        users['items'].extend([
            {
                "type": "divider"
            },
            {
                "type": "link",
                "href": "/invitations/geonode-send-invite/",
                "label": "Invite users"
            },
            {
                "type": "link",
                "href": "/admin/people/profile/add/",
                "label": "Add user"
            } if user.is_superuser else None,
            {
                "type": "link",
                "href": "/groups/create/",
                "label": "Create group"
            } if user.is_superuser else None,
        ])

    return [
        {
            "label": "Data",
            "type": "dropdown",
            "items": [
                {
                    "type": "link",
                    "href": "/catalogue/#/search/?f=dataset",
                    "label": "Map Layers"
                },
                {
                    "type": "link",
                    "href": "/catalogue/#/search/?f=document",
                    "label": "Documents"
                } if not is_mobile else None,
                {
                    "type": "link",
                    "href": "/services/",
                    "label": "Remote Services"
                } if is_logged_in else None,
                {
                    "type": "divider"
                } if is_logged_in else None,
                {
                    "type": "link",
                    "href": "/catalogue/#/upload/dataset",
                    "label": "Upload Map Layers"
                } if is_logged_in else None,
                {
                    "type": "link",
                    "href": "/catalogue/#/upload/document",
                    "label": "Upload Document"
                } if is_logged_in else None,
                {
                    "type": "link",
                    "href": "/services/register/",
                    "label": "Add Remote Services"
                } if is_logged_in else None,
                {
                    "type": "divider"
                },
                {
                    "type": "link",
                    "href": "/view/well-and-monitoring-data/",
                    "label": "Well and Monitoring Data"
                },
                {
                    "type": "dropdown",
                    "label": "Upload Well and Monitoring Data",
                    "items": [{
                        "type": "link",
                        "href": "/groundwater/record/create/",
                        "label": "Add Record"
                    }, {
                        "type": "link",
                        "href": "/groundwater/batch-upload",
                        "label": "Batch Upload"
                    }]
                } if is_logged_in else None,
                {
                    "type": "link",
                    "href": "/groundwater/record/download-request",
                    "label": "Download Well and Monitoring Data",
                },
            ]
        },
        {
            "type": "link",
            "href": "/catalogue/#/search/?f=map",
            "label": "Maps"
        },
        {
            "type": "link",
            "href": "/catalogue/#/search/?f=dashboard",
            "label": "Dashboards"
        },
        {
            "type": "link",
            "href": "/catalogue/#/search/?f=geostory",
            "label": "GeoStories"
        },
        users,
        {
            "type": "link",
            "href": "/about",
            "label": "About"
        }
    ]


@register.simple_tag(
    takes_context=True, name='get_igrac_base_right_topbar_menu')
def get_igrac_base_right_topbar_menu(context):
    return []


@register.simple_tag(takes_context=True)
def get_igrac_user_menu(context):
    profile = get_user_menu(context)
    user = context.get('request').user
    profile[0]['label'] = user.full_name_or_nick
    profile[0]['variant'] = 'primary'
    for idx, item in enumerate(profile[0]['items']):
        try:
            if item['label'] == 'GeoServer':
                profile[0]['items'].insert(
                    idx + 1,
                    {'type': 'link', 'href': '/cms/', 'label': 'Wagtail Admin'}
                )
        except KeyError:
            pass
    return profile