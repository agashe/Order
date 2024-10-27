from django import template

register = template.Library()

@register.filter
# Original Source : https://stackoverflow.com/a/66553800
def replace(value, arg):
    search, replace = arg.split('|')
    return value.replace(search, replace)