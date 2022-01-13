from django import template
from django.template.defaultfilters import stringfilter
from apps.users.models import MONTH_CHOICES
from apps.jobs.models import JobPostingApplicant

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


@register.filter()
def filter_postings(queryset, _id):
    postings = JobPostingApplicant.objects.filter(
        applicant__id=_id).values_list('company_job', flat=True)
    queryset.exclude(id__in=postings)
    return queryset.exclude(id__in=postings)
