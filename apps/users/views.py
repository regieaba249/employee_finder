from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.generic.edit import (
    FormView,
    CreateView,
    UpdateView
)

from .forms import LoginForm, UserForm
from .models import (
    CustomUser,
    Applicant,
    ApplicantAttachments
)
from .tokens import account_activation_token
from apps.companies.models import Company

User = get_user_model()


def test(request):
    send_mail(
        'test',
        'test',
        settings.EMAIL_HOST_USER,
        ['regieaba249@gmail.com'],
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
            "Thank you for your email confirmation. Now you can login to your account."
        )
    else:
        messages.error(
            request,
            "Activation Failed. Activation link is invalid!"
        )

    return HttpResponseRedirect(reverse_lazy('login'))


class LoginView(FormView):
    """login view"""

    form_class = LoginForm
    redirect_authenticated_user = True
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('jobs:jobs-board'))
        return super(LoginView, self).get(request, *args, **kwargs)


    def get_success_url(self):
        return reverse_lazy(
            'users:profile',
            kwargs={'pk': self.request.user.pk}
        )


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


class RegistrationView(FormView):
    """registration view"""

    form_class = UserForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')
    template_name = 'registration.html'

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        context['user_type'] = self.kwargs.get('_type')
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

        if form.is_valid():
            form.save()
            if user_type == 'applicant':
                applicant_data = {
                    'user': user,
                    'applicant_status': applicant_status,
                    'resume': resume,
                }
                applicant = Applicant.objects.create(**applicant_data)

                for f in files:
                    applicant_data = {
                        'applicant': applicant,
                        'attachment': f,
                    }
                    ApplicantAttachments.objects.create(**applicant_data)
            else:

                company_data = {
                    'owner': user,
                    'name': form.data.get('company_name', ''),
                    'address': form.data.get('company_name', ''),
                    'founded_on': form.data.get('founded_on', ''),
                    'website': form.data.get('website', ''),
                    'overview': form.data.get('company_overview', ''),
                    'employee_count': form.data.get('employee_count', ''),
                    'company_avatar': company_avatar,
                }
                company = Company.objects.create(**company_data)

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
                fail_silently=False,
            )

            return res
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('jobs:jobs-board'))
        return super(RegistrationView, self).get(request, *args, **kwargs)

    def form_invalid(self, form):
        for key, value in form.errors.items():
            for msg in value:
                messages.error(self.request, f"{key}: {msg}")
        return super(RegistrationView, self).form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Successfully Created your Account")
        return super(RegistrationView, self).form_valid(form)


class CustomUserUpdateView(UpdateView):

    model = CustomUser
    fields = '__all__'
    template_name = 'user_profile.html'

    def get_success_url(self):
        return reverse_lazy(
            'users:profile',
            kwargs={'pk': self.request.user.pk}
        )

    def get_context_data(self, **kwargs):
        context = super(CustomUserUpdateView, self).get_context_data(**kwargs)
        obj = self.model.objects.get(pk=self.kwargs.get('pk'))
        context['resume'] = obj.applicant_data.resume
        context['attachment_objs'] = ApplicantAttachments.objects.filter(applicant=obj.applicant_data)
        return context

    # def post(self, request, *args, **kwargs):
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     user = form.instance
    #     resume = request.FILES.get('resume')
    #     files = request.FILES.getlist('attachments')
    #     applicant_status = form.data.get('applicant_status', '')
    #     token = account_activation_token.make_token(user)
    #     form.instance.token = token

    #     if form.is_valid():
    #         form.save()
    #         if self.request.path == '/users/register/applicant/':
    #             applicant_data = {
    #                 'user': user,
    #                 'applicant_status': applicant_status,
    #                 'resume': resume,
    #             }
    #             applicant = Applicant.objects.create(**applicant_data)

    #             for f in files:
    #                 applicant_data = {
    #                     'applicant': applicant,
    #                     'attachment': f,
    #                 }
    #                 ApplicantAttachments.objects.create(**applicant_data)
    #         else:
    #             pass

    #         res = self.form_valid(form)

    #         current_site = get_current_site(request)
    #         mail_subject = 'Activate your account'
    #         message = render_to_string('acc_active_email.html', {
    #             'user': user,
    #             'domain': current_site.domain,
    #             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    #             'token': token,
    #         })
    #         to_email = form.cleaned_data.get('email')
    #         send_mail(
    #             mail_subject,
    #             message,
    #             settings.EMAIL_HOST_USER,
    #             [to_email],
    #             fail_silently=False,
    #         )

    #         return res
    #     else:
    #         return self.form_invalid(form)

    def form_invalid(self, form):
        for key, value in form.errors.items():
            for msg in value:
                messages.error(self.request, f"{key}: {msg}")

        return super(CustomUserUpdateView, self).form_invalid(form)

    def form_valid(self, form):
        """ process user login"""
        context = super(CustomUserUpdateView, self).form_valid(form)
        return context
