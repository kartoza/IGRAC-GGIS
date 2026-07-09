from django import template

register = template.Library()


@register.filter(name='thousands')
def thousands(value):
    """Format a number with thousands separator, e.g. 2000000 -> 2,000,000."""
    try:
        return '{:,}'.format(int(value))
    except (TypeError, ValueError):
        return value