from datetime import datetime

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from apps.users.models import (
    CustomUser,
    Applicant,
    ApplicantExperience
)
from .models import (
    CompanyJobPosting,
    JobPostingApplicant
)


def ajax_add_to_posting(request):
    applicant_id = request.GET.get('applicant_id')
    applicant = Applicant.objects.get(id=applicant_id)
    posting_id = request.GET.get('posting_id')
    posting = CompanyJobPosting.objects.get(id=posting_id)

    data = {
        'company_job': posting,
        'applicant': applicant,
    }
    JobPostingApplicant.objects.create(**data)

    return JsonResponse({
        'success': True,
    })


def ajax_archive_postings(request):
    _id = request.GET.get('_id')
    posting = CompanyJobPosting.objects.filter(id=_id)
    posting.update(is_active=False)

    return JsonResponse({
        'success': True,
    })


def ajax_filter_postings(request):
    _input = request.GET.get('_input')
    queryset = CompanyJobPosting.objects.filter(
        Q(job_title__contains=_input)
        | Q(description__contains=_input)
        | Q(employment_type__contains=_input)
        | Q(company__name__contains=_input)
    )

    html_str = ""
    for posting in queryset:
        html_str += render_to_string('job_posting_item.html', {
            'posting': posting,
            'user': request.user
        })

    return JsonResponse({
        'success': True,
        'htmlStr': html_str,
    })


def ajax_hire_applicant(request):
    user_id = request.GET.get('user_id')
    posting_id = request.GET.get('posting_id')
    user = CustomUser.objects.get(id=user_id)
    job_posting = CompanyJobPosting.objects.get(id=posting_id)

    # Update job applicant status to hired
    job_posting_applicant = JobPostingApplicant.objects.filter(
        company_job=job_posting,
        applicant=user.applicant_data
    )
    job_posting_applicant.update(status='hired')

    # Update status to employed
    Applicant.objects.filter(user=user).update(applicant_status='employed')

    # Email
    mail_subject = f'Hired for position: {job_posting.job_title}'
    message = render_to_string('hired_email.html', {
        'user': user,
        'hiring_agent': job_posting.company.owner,
        'job_posting': job_posting,
        # 'job_posting_link': reverse_lazy('users:profile_edit', kwargs={'pk': request.user.pk})
        'job_posting_link': ""
    })
    to_email = job_posting.company.owner.email
    send_mail(
        mail_subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email],
        fail_silently=True,
    )

    # Create Experience Record
    start_month = datetime.now().strftime("%b").lower()
    start_year = datetime.now().year

    data = {
        'applicant': user.applicant_data,
        'company_name': job_posting.company.name,
        'job_position': job_posting.job_title,
        'employment_type': job_posting.employment_type,
        'start_month': start_month,
        'start_year': start_year,
        'end_month': '',
        'end_year': '',
        'current': True,
        'description': job_posting.description,
        'reference_person': job_posting.company.owner.full_name,
        'mobile_number': job_posting.company.owner.mobile_number,
    }
    ApplicantExperience.objects.create(**data)

    return JsonResponse({
        'success': True,
    })


def ajax_decline_applicant(request):
    user_id = request.GET.get('user_id')
    posting_id = request.GET.get('posting_id')
    user = CustomUser.objects.get(id=user_id)
    job_posting = CompanyJobPosting.objects.get(id=posting_id)

    job_posting_applicant = JobPostingApplicant.objects.filter(
        company_job=job_posting,
        applicant=user.applicant_data
    )
    job_posting_applicant.update(status='declined')

    mail_subject = f'Declined for position: {job_posting.job_title}'
    message = render_to_string('declined_email.html', {
        'user': request.user,
        'hiring_agent': job_posting.company.owner,
        'job_posting': job_posting,
        # 'job_posting_link': reverse_lazy('users:profile_edit', kwargs={'pk': request.user.pk})
        'job_posting_link': ""
    })

    to_email = job_posting.company.owner.email
    send_mail(
        mail_subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email],
        fail_silently=True,
    )
    return JsonResponse({
        'success': True,
    })


def ajax_schedule_interview(request):
    user_id = request.GET.get('user_id')
    posting_id = request.GET.get('posting_id')
    date = request.GET.get('date')

    user = CustomUser.objects.get(id=user_id)
    job_posting = CompanyJobPosting.objects.get(id=posting_id)

    mail_subject = f'Scheduled Interview for job title: {job_posting.job_title}'
    message = render_to_string('schedule_interview_email.html', {
        'user': user,
        'hiring_agent': job_posting.company.owner,
        'job_posting': job_posting,
        'interview_date': date,
        # 'job_posting_link': reverse_lazy('users:profile_edit', kwargs={'pk': request.user.pk})
        'job_posting_link': ""
    })

    to_email = job_posting.company.owner.email
    msg = EmailMessage(
        mail_subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email],

    )
    msg.content_subtype = "html"
    for file in job_posting.job_posting_attachments.all():
        msg.attach_file(file.attachment.url[1:])
    msg.send()

    job_posting_applicant = JobPostingApplicant.objects.filter(
        company_job=job_posting,
        applicant=user.applicant_data
    )
    job_posting_applicant.update(status='interview')

    return JsonResponse({
        'success': True,
    })


def ajax_apply(request):
    _id = request.GET.get('id')
    action = request.GET.get('action')
    job_posting = CompanyJobPosting.objects.get(id=_id)

    data = {
        'company_job': job_posting,
        'applicant': request.user.applicant_data,
    }
    if action == 'apply':
        JobPostingApplicant.objects.create(**data)
    else:
        applicants = JobPostingApplicant.objects.filter(**data)
        applicants.delete()

    mail_subject = f'New Applicant for position: {job_posting.job_title}'
    message = render_to_string('new_applicant_email.html', {
        'user': request.user,
        'hiring_agent': job_posting.company.owner,
        'job_posting': job_posting,
        'user_profile': reverse_lazy('users:profile_edit',
                                     kwargs={'pk': request.user.pk})
    })

    to_email = job_posting.company.owner.email
    send_mail(
        mail_subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email],
        fail_silently=True,
    )

    applicantsStr = ""
    for applicant in job_posting.job_applicants.all():
        applicantsStr += render_to_string('new_applicant_email.html', {
            'job_applicant': request.user,
            'posting': job_posting,
        })

    return JsonResponse({
        'success': True,
        'applicantsStr': applicantsStr,
    })


class JobsBoardView(LoginRequiredMixin, TemplateView):
    template_name = 'jobs_board.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.user_type == 'applicant':
            context['latest_jobs'] = CompanyJobPosting.objects.all().order_by('-created_at')
        else:
            context['latest_jobs'] = self.request.user.company_data.company_jobs.all()
        return context
