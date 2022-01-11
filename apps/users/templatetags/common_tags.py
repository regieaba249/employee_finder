from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter()
@stringfilter
def blankifnull(value):
    if not value or value == 'None':
        return ''
    return value


@register.filter()
def test(value):
    import pdb; pdb.set_trace()
    return True
