from django import template

register = template.Library()


@register.filter(name='remove_localhost')
def remove_localhost(url):
    """Remove localhost from url"""
    if url:
        url = url.replace('http://localhost:8080', '')
    return url
