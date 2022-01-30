from datetime import datetime
from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.views.generic.edit import (
    FormView,
    CreateView,
    UpdateView
)
from apps.companies.models import Company

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
)
from apps.users.forms import (
    UpdateForm
)
from employee_finder.helpers import (
    EMPLOYMENT_TYPE_CHOICES,
    MONTH_CHOICES,
    AREA_CODES
)


# Create your views here.
class CompanyUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):

    model = CustomUser
    form_class = UpdateForm
    template_name = 'company_profile_update.html'

    def test_func(self):
        user_id = self.kwargs.get('pk')
        return self.request.user.id == user_id

    def get_success_url(self):
        return reverse_lazy(
            'companies:profile_edit',
            kwargs={'pk': self.request.user.pk}
        )

    def get_context_data(self, **kwargs):
        context = super(CompanyUpdateView, self).get_context_data(**kwargs)
        company = self.object.company_data

        context['area_codes'] = AREA_CODES
        context['months'] = dict(MONTH_CHOICES)
        year = datetime.today().year
        context['years'] = list(range(year, year - 50, -1))
        context['employment_type_choices'] = dict(EMPLOYMENT_TYPE_CHOICES)

        _region = context['form'].instance.region
        _province = context['form'].instance.province
        _municipality = context['form'].instance.municipality

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

        context['job_postings'] = company.company_jobs.all().order_by('-created_at')

        return context

    def post(self, request, *args, **kwargs):
        res = super(CompanyUpdateView, self).post(request, *args, **kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        company = form.instance.company_data

        name = form.data.get('company_name', '')
        website = form.data.get('website', '')
        overview = form.data.get('company_overview', '')
        employee_count = form.data.get('employee_count', '')
        email = form.data.get('company_email', '')
        phone_number = form.data.get('company_phone_number', '')
        mobile_number = form.data.get('company_mobile_number', '')

        company_data = {
            'name': name,
            'website': website,
            'overview': overview,
            'employee_count': employee_count,
            'email': email,
            'phone_number': phone_number,
            'mobile_number': mobile_number
        }

        if form.data.get('founded_on', None):
            company_data['founded_on'] = form.data.get('founded_on')

        # Update Applicant Data
        Company.objects.filter(id=company.id).update(**company_data)

        return res

    def form_invalid(self, form):
        for key, value in form.errors.items():
            for msg in value:
                messages.error(self.request, f"{key}: {msg}")
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        """ process user login"""
        context = super(CompanyUpdateView, self).form_valid(form)
        messages.success(self.request, "Successfully Updated your Company details")
        return context
