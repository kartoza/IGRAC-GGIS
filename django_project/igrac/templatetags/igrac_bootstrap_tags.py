from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def field_as_bootstrap(field):
    name = field.name
    if not name.startswith("radio") and not name.startswith("checkbox"):
        try:
            field.field.widget.attrs["class"] += " form-control"
        except KeyError:
            field.field.widget.attrs["class"] = " form-control"

    return mark_safe(
        f'<div id="{field.id_for_label}" class="form-group {"has-error" if field.errors else ""}">'
        f'<label for="{field.id_for_label}" class="control-label {"required-field" if field.field.required else ""}">{field.label}</label>'
        f'{field}'
        f'<div class="error-msg">{field.errors}</div>'
        f'<div class="help-text">{field.help_text}</div>'
        '</div>'
    )
