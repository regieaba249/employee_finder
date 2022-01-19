from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import (HttpResponseRedirect, JsonResponse)
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.generic.base import TemplateView
from django.views.generic.edit import (
    FormView,
    CreateView,
    UpdateView
)
from .tokens import account_activation_token
from .forms import (
    LoginForm,
    RegistrationForm,
    UpdateForm
)
from apps.companies.models import Company
from apps.jobs.models import (
    JobPostingApplicant,
    CompanyJobPosting
)
from .models import (
    CustomUser,
    Applicant,
    ApplicantAttachment,
    ApplicantExperience,
    ApplicantEducation,
    ApplicantSkill,
    Region,
    Province,
    Municipality,
    Barangay,

    # choices
    EMPLOYMENT_TYPE_CHOICES,
    MONTH_CHOICES,
)

from employee_finder.helpers import (
    EFFICIENCY_CHOICES,
    MONTH_CHOICES
)


User = get_user_model()

Tables = {
    'CustomUser': CustomUser,
    'Applicant': Applicant,
    'ApplicantAttachment': ApplicantAttachment,
    'ApplicantExperience': ApplicantExperience,
    'ApplicantEducation': ApplicantEducation,
    'JobPostingApplicant': JobPostingApplicant,
    'CompanyJobPosting': CompanyJobPosting,
    'Region': Region,
    'Province': Province,
    'Municipality': Municipality,
    'Barangay': Barangay,
}


def test(request):
    send_mail(
        'test',
        'test',
        settings.EMAIL_HOST_USER,
        ['test@test.com'],
        fail_silently=False,
    )


def Logout(request):
    """logout logged in user"""
    logout(request)
    return HttpResponseRedirect(reverse_lazy('login'))


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid, token=token)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None:
        user.is_active = True
        user.save()
        messages.success(
            request,
            "Thank you for your email confirmation. You can now login to your account."
        )
    else:
        messages.error(
            request,
            "Activation Failed. Activation link is invalid!"
        )

    return HttpResponseRedirect(reverse_lazy('login'))


def ajax_check_password(request):
    password1 = request.GET.get("password1")
    password2 = request.GET.get("password2")
    MIN_LENGTH = 8
    valid = True
    _type = ""
    message = ""

    if password1 and password2 and password1 != password2:
        return JsonResponse({
            'valid': False,
            'type': 'match',
            'message': "Passwords don't match!",
        })

    # At least MIN_LENGTH long
    first_isalpha = password1[0].isalpha()
    if (len(password1) < MIN_LENGTH) or all(c.isalpha() == first_isalpha for c in password1):
        return JsonResponse({
            'valid': False,
            'type': 'format',
            'message': f"Password must be at least {MIN_LENGTH} characters, with atleast one capital and digit or punctuation.",
        })

    return JsonResponse({
        'valid': valid,
        'type': _type,
        'message': message,
    })


def ajax_check_email(request):
    email = request.GET.get('email')
    exists = CustomUser.objects.filter(email=email).exists()

    return JsonResponse({
        'exists': exists,
    })

def ajax_load_address_dropdown(request):

    select_id = request.GET.get('_id')
    value = request.GET.get('value')
    target_name = request.GET.get('target_name')

    data = {
        "province": Province.objects.filter(
            region__id=select_id).order_by('name'),
        "municipality": Municipality.objects.filter(
            province__id=select_id).order_by('name'),
        "barangay": Barangay.objects.filter(
            municipality__id=select_id).order_by('name'),
    }

    return render(
        request,
        'dropdown_list_options.html',
        {
            'items': data[target_name],
            'value': value
        }
    )


def ajax_add_employment_history(request):

    company = request.GET.get('company')
    position = request.GET.get('position')
    employment_type = request.GET.get('employment_type')
    start_month = request.GET.get('start_month')
    start_year = request.GET.get('start_year')
    end_month = request.GET.get('end_month')
    end_year = request.GET.get('end_year')
    current = bool(request.GET.get('current'))
    overview = request.GET.get('overview')
    reference_person = request.GET.get('reference_person')
    mobile_number = request.GET.get('mobile_number')

    if mobile_number == "+63":
        mobile_number = None

    data = {
        'applicant': request.user.applicant_data,
        'company_name': company,
        'job_position': position,
        'employment_type': employment_type,
        'start_month': start_month,
        'start_year': start_year,
        'end_month': end_month,
        'end_year': end_year,
        'current': current,
        'description': overview,
        'reference_person': reference_person,
        'mobile_number': mobile_number,
    }
    ApplicantExperience.objects.create(**data)

    queryset = ApplicantExperience.objects.filter(
        applicant=request.user.applicant_data
    ).order_by('-current', '-start_month', '-start_year').values()

    return JsonResponse({
        'success': True,
        'items': list(queryset),
        'types': dict(EMPLOYMENT_TYPE_CHOICES),
        'months': dict(MONTH_CHOICES)
    })


def ajax_add_skill(request):
    user_id = request.POST.get('_id')
    school_name = request.POST.get('school_name')
    efficiency = request.POST.get('efficiency')
    file = request.FILES.get('file')

    user = CustomUser.objects.get(id=user_id)
    data = {
        'applicant': user.applicant_data,
        'name': school_name,
        'efficiency': efficiency,
        'attachment': file,
    }
    ApplicantSkill.objects.create(**data)

    queryset = ApplicantSkill.objects.filter(
        applicant=request.user.applicant_data
    ).values()

    return JsonResponse({
        'success': True,
        'items': list(queryset),
    })


def ajax_add_education(request):
    school_name = request.GET.get('school_name')
    degree = request.GET.get('degree')
    start_month = request.GET.get('start_month')
    start_year = request.GET.get('start_year')
    end_month = request.GET.get('end_month')
    end_year = request.GET.get('end_year')
    reference_person = request.GET.get('reference_person')
    mobile_number = request.GET.get('mobile_number')

    if mobile_number == "+63":
        mobile_number = None

    data = {
        'applicant': request.user.applicant_data,
        'school_name': school_name,
        'degree': degree,
        'start_month': start_month,
        'start_year': start_year,
        'end_month': end_month,
        'end_year': end_year,
        'reference_person': reference_person,
        'mobile_number': mobile_number,
    }
    ApplicantEducation.objects.create(**data)

    queryset = ApplicantEducation.objects.filter(
        applicant=request.user.applicant_data
    ).order_by('-start_month', '-start_year').values()

    return JsonResponse({
        'success': True,
        'items': list(queryset),
        'months': dict(MONTH_CHOICES)
    })


def ajax_delete_data(request):

    _id = request.GET.get('id')
    table = Tables[request.GET.get('table')]

    record = table.objects.get(id=_id)
    record.delete()

    return JsonResponse({'success': True})


def ajax_delete_attachment(request):

    _id = request.GET.get('id')
    _type = request.GET.get('type')

    if _type == "resume":
        Applicant.objects.filter(id=_id).update(resume=None)
    else:
        record = ApplicantAttachment.objects.get(id=_id)
        record.delete()

    return JsonResponse({'success': True})


class LoginView(FormView):
    """login view"""

    form_class = LoginForm
    redirect_authenticated_user = True
    template_name = 'login.html'
    success_url = reverse_lazy('jobs:jobs_board',)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('jobs:jobs_board'))
        return super(LoginView, self).get(request, *args, **kwargs)

    def form_invalid(self, form):
        for key, value in form.errors.items():
            for msg in value:
                messages.error(self.request, f"{key}: {msg}")

        return super(LoginView, self).form_invalid(form)

    def form_valid(self, form):
        """ process user login"""
        user = authenticate(username=form.cleaned_data['email'],
                            password=form.cleaned_data['password'])

        if user is not None:
            if user.is_active:
                login(self.request, user)
                if form.cleaned_data['remember_me']:
                    self.request.session.set_expiry(1209600)
                return HttpResponseRedirect(self.get_success_url())
            else:
                messages.error(self.request, 'Please activate your account.')
        else:
            messages.error(self.request, 'Please check your credentials')

        return HttpResponseRedirect(reverse_lazy('login'))


class RegistrationView(LoginRequiredMixin, FormView):
    """registration view"""

    form_class = RegistrationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')
    template_name = 'registration.html'

    def get_context_data(self, *args, **kwargs):
        context = super(RegistrationView, self).get_context_data(*args, **kwargs)
        context['user_type'] = self.kwargs.get('_type')
        context['area_codes'] = ['02', '032', '033', '034', '035', '036',
                                 '038', '042', '043', '044', '045', '046',
                                 '047', '048', '049', '052', '053', '054',
                                 '055', '056', '062', '063', '064', '065',
                                 '068', '072', '074', '075', '077', '078',
                                 '082', '083', '084', '085', '086', '087',
                                 '088', '08822', '08842']
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

        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        user = form.instance
        resume = request.FILES.get('resume')
        company_avatar = request.FILES.get('company_avatar')
        files = request.FILES.getlist('attachments')
        applicant_status = form.data.get('applicant_status', '')
        token = account_activation_token.make_token(user)
        form.instance.token = token

        user_type = 'applicant'
        if self.request.path == '/users/register/employer/':
            user_type = 'employer'

        form.instance.user_type = user_type
        if form.data.get('mobile_number', None):
            form.instance.mobile_number = f"+63{form.data.get('mobile_number')}"

        if form.is_valid():

            # if form.data.get('region', None):
            #     form.instance.region = Region.objects.get(id=form.data.get('region'))

            # if form.data.get('province', None):
            #     form.instance.province = Province.objects.get(id=form.data.get('province'))

            # if form.data.get('municipality', None):
            #     form.instance.municipality = Municipality.objects.get(id=form.data.get('municipality'))

            # if form.data.get('barangay', None):
            #     form.instance.barangay = Barangay.objects.get(id=form.data.get('barangay'))

            form.save()
            if user_type == 'applicant':
                applicant_data = {
                    'user': user,
                    'applicant_status': applicant_status,
                    'resume': resume,
                }
                applicant = Applicant.objects.create(**applicant_data)

                for f in files:
                    attachment_data = {
                        'applicant': applicant,
                        'attachment': f,
                    }
                    ApplicantAttachment.objects.create(**attachment_data)
            else:

                company_data = {
                    'owner': user,
                    'name': form.data.get('company_name', ''),
                    'website': form.data.get('website', ''),
                    'overview': form.data.get('company_overview', ''),
                    'email': form.data.get('company_email', ''),
                    'phone_number': form.data.get('company_phone_number', ''),
                    'mobile_number': form.data.get('company_mobile_number', '')
                }

                if form.data.get('founded_on', None):
                    company_data['founded_on'] = form.data.get('founded_on')

                if form.data.get('employee_count', None):
                    company_data['employee_count'] = form.data.get('employee_count')

                Company.objects.create(**company_data)

            res = self.form_valid(form)

            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })
            to_email = form.cleaned_data.get('email')
            send_mail(
                mail_subject,
                message,
                settings.EMAIL_HOST_USER,
                [to_email],
                fail_silently=True,
            )

            return res
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('jobs:jobs_board'))
        return super(RegistrationView, self).get(request, *args, **kwargs)

    def form_invalid(self, form):
        for key, value in form.errors.items():
            for msg in value:
                messages.error(self.request, f"{key}: {msg}")
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        messages.success(self.request, "Successfully Registered. Please validate via the email we sent to activate your account.")
        return super(RegistrationView, self).form_valid(form)


class CustomUserUpdateView(LoginRequiredMixin, UpdateView):

    model = CustomUser
    form_class = UpdateForm
    template_name = 'user_profile_update.html'

    def get_success_url(self):
        return reverse_lazy(
            'users:profile_edit',
            kwargs={'pk': self.request.user.pk}
        )

    def get_context_data(self, **kwargs):
        context = super(CustomUserUpdateView, self).get_context_data(**kwargs)
        applicant = self.object.applicant_data

        # Static Values
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
            'dec': 'December',}
        year = datetime.today().year
        context['years'] = list(range(year, year - 50, -1))
        context['employment_type_choices'] = dict(EMPLOYMENT_TYPE_CHOICES)
        context['efficiency_choices'] = dict(EFFICIENCY_CHOICES)

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
            context['barangays'] = Barangay.objects.filter(
                municipality=_municipality)
        else:
            context['barangays'] = Barangay.objects.all()

        context['employment_history'] = applicant.applicant_experience.all(
        ).order_by('-current', '-start_month', '-start_year')
        context['educational_history'] = applicant.applicant_education.all(
        ).order_by('-start_month', '-start_year')
        context['skills'] = applicant.applicant_skills.all()

        return context

    def post(self, request, *args, **kwargs):
        res = super(CustomUserUpdateView, self).post(request, *args, **kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        applicant = form.instance.applicant_data

        resume = request.FILES.get('resume')
        files = request.FILES.getlist('attachments')
        applicant_status = form.data.get('applicant_status', '')
        overview = form.data.get('overview', '')

        # Update Applicant Data
        Applicant.objects.filter(id=applicant.id).update(
            resume=resume,
            applicant_status=applicant_status,
            overview=overview
        )

        for file in files:
            ApplicantAttachment.objects.create(
                applicant=applicant,
                attachment=file
            )

        return res

    def form_invalid(self, form):
        for key, value in form.errors.items():
            for msg in value:
                messages.error(self.request, f"{key}: {msg}")
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        """ process user login"""
        context = super(CustomUserUpdateView, self).form_valid(form)
        messages.success(self.request, "Successfully Updated your profile details")
        return context


class ApplicantBoardView(LoginRequiredMixin, TemplateView):
    template_name = 'applicants_board.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_applicants'] = Applicant.objects.all().order_by('-created_at')
        context['postings'] = CompanyJobPosting.objects.filter(
            company=self.request.user.company_data).order_by('-created_at')
        return context
