from django import template
from django.template.defaultfilters import stringfilter
from apps.users.models import MONTH_CHOICES

register = template.Library()


@register.filter()
@stringfilter
def blankifnull(value):
    if not value or value == 'None':
        return ''
    return value


@register.filter()
@stringfilter
def to_month_string(x):
    months = dict(MONTH_CHOICES)
    return months[x]


@register.filter()
def test(value):
    import pdb; pdb.set_trace()
    return True
