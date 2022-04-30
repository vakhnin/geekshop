from django import template

register = template.Library()


@register.filter(name='startswith')
def startswith(text, starts):
    return str(text).startswith(starts)
