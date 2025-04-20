from django import template
import re

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    """Add a CSS class to a form field."""
    if hasattr(value, 'field') and hasattr(value.field, 'widget'):
        if value.field.widget.attrs.get('class', None):
            value.field.widget.attrs['class'] += ' ' + css_class
        else:
            value.field.widget.attrs['class'] = css_class
    return value

@register.filter(name='strip_tags')
def strip_tags(value):
    """Strip HTML tags from a string."""
    return re.sub(r'<[^>]*?>', '', str(value or ''))

@register.filter(name='split')
def split(value, separator):
    """Split a string by a separator."""
    if value is None:
        return []
    return str(value).split(separator)