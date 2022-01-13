from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import (
    FormView,
    CreateView,
    UpdateView
)

from apps.jobs.models import (
    CompanyJobPosting,
    JobPostingAttachment
)
from apps.users.models import (
    CustomUser,
    Region,
    Province,
    Municipality,
    Barangay,
    EMPLOYMENT_TYPE_CHOICES
)


# Create your views here.
def ajax_add_job_posting(request):

    job_title = request.POST.get('job_title')
    description = request.POST.get('description')
    vacancy = request.POST.get('vacancy')
    salary_range_end = request.POST.get('salary_range_end')
    salary_range_start = request.POST.get('salary_range_start')
    attachments = request.FILES.getlist('files')

    data = {
        'company': request.user.company_data,
        'job_title': job_title,
        'description': description,
        'vacancy': vacancy,
        'salary_range_end': salary_range_end,
        'salary_range_start': salary_range_start,
    }
    posting = CompanyJobPosting.objects.create(**data)

    for file in attachments:
        data = {
            'job_posting': posting,
            'attachment': file,
        }
        JobPostingAttachment.objects.create(**data)

    postings = CompanyJobPosting.objects.filter(
        company=request.user.company_data
    ).order_by('-created_at').values()

    attachments = JobPostingAttachment.objects.filter(
        job_posting=posting
    ).order_by('-created_at').values()

    return JsonResponse({
        'success': True,
        'items': list(postings),
        'attachments': list(attachments),
    })


class CompanyUpdateView(UpdateView):

    model = CustomUser
    fields = '__all__'
    template_name = 'company_profile_update.html'

    def get_success_url(self):
        return reverse_lazy(
            'company:profile_edit',
            kwargs={'pk': self.request.user.pk}
        )

    def get_context_data(self, **kwargs):
        context = super(CompanyUpdateView, self).get_context_data(**kwargs)
        obj = self.model.objects.get(pk=self.kwargs.get('pk'))
        context['area_codes'] = ['02', '032', '033', '034', '035', '036',
                                 '038', '042', '043', '044', '045', '046',
                                 '047', '048', '049', '052', '053', '054',
                                 '055', '056', '062', '063', '064', '065',
                                 '068', '072', '074', '075', '077', '078',
                                 '082', '083', '084', '085', '086', '087',
                                 '088', '08822', '08842']
        context['months'] = {
            'jan': 'January',
            'feb': 'February',
            'mar': 'March',
            'apr': 'April',
            'may': 'May',
            'jun': 'June',
            'jul': 'July',
            'aug': 'August',
            'sep': 'September',
            'oct': 'October',
            'nov': 'November',
            'dec': 'December',
        }

        year = datetime.today().year
        context['years'] = list(range(year, year - 50, -1))

        _region = context['form'].instance.region
        _province = context['form'].instance.province
        _municipality = context['form'].instance.municipality
        _barangay = context['form'].instance.barangay

        context['regions'] = Region.objects.all()
        if _region:
            context['provinces'] = Province.objects.filter(region=_region)
        else:
            context['provinces'] = Province.objects.all()

        if _province:
            context['municipalities'] = Municipality.objects.filter(province=_province)
        else:
            context['municipalities'] = Municipality.objects.all()

        if _municipality:
            context['barangays'] = Barangay.objects.filter(municipality=_municipality)
        else:
            context['barangays'] = Barangay.objects.all()

        context['job_postings'] = CompanyJobPosting.objects.filter(
            company=obj.company_data
        ).order_by('-created_at')

        context['employment_type_choices'] = dict(EMPLOYMENT_TYPE_CHOICES)

        return context
