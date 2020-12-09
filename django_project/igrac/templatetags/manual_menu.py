from django import template
from django.utils.safestring import mark_safe

register = template.Library()


def get_list_element(list_data, active_slug):
    element = '<ul>'
    for data in list_data:
        element += '<li {c}><a href="{url}" >{title}</a>'.format(
            url=data['url'],
            title=data['title'],
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
