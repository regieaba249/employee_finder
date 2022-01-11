from datetime import datetime

from django.shortcuts import render
from django.views.generic.edit import (
    FormView,
    CreateView,
    UpdateView
)

from .models import Company
from apps.users.models import (
    Region,
    Province,
    Municipality,
    Barangay,
)

# Create your views here.


class CompanyUpdateView(UpdateView):

    model = Company
    fields = '__all__'
    template_name = 'company_profile.html'

    def get_success_url(self):
        return reverse_lazy(
            'company:profile',
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

        _region = context['form'].instance.owner.region
        _province = context['form'].instance.owner.province
        _municipality = context['form'].instance.owner.municipality
        _barangay = context['form'].instance.owner.barangay

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

        return context
