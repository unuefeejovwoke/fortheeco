from django import template

register = template.Library()

@register.filter
def dict_get(value, key):
    return value.get(key, '')
