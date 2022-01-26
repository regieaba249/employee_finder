import django
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
    ApplicantExperience,
    Region,
    Province,
    Municipality,
    Barangay,
)
from .models import (
    CompanyJobPosting,
    JobPostingApplicant,
    JobPostingAttachment
)
from employee_finder.helpers import EMPLOYMENT_TYPE_CHOICES


def ajax_get_candidates(request):
    _id = request.GET.get('_id')
    searchInput = None if request.GET.get('filters[searchInput]') == '' else request.GET.get('filters[searchInput]')
    filter_status = request.GET.get('filters[filter_status]', None)
    filter_years = None if request.GET.get('filters[filter_years]') == '' else request.GET.get('filters[filter_years]')
    filter_gender = None if request.GET.get('filters[filter_gender]') == '' else request.GET.get('filters[filter_gender]')
    user_region = None if request.GET.get('filters[user_region]') == '' else request.GET.get('filters[user_region]')
    user_province = None if request.GET.get('filters[user_province]') == '' else request.GET.get('filters[user_province]')
    user_municipality = None if request.GET.get('filters[user_municipality]') == '' else request.GET.get('filters[user_municipality]')

    if any([searchInput,
            filter_status,
            filter_years,
            filter_gender,
            user_region,
            user_province,
            user_municipality]):

        q = Q()
        if filter_status:
            q &= Q(applicant_status=filter_status)
        if filter_gender:
            q &= Q(user__gender=filter_gender)
        if user_region:
            q &= Q(user__region__id=user_region)
        if user_province:
            q &= Q(user__province__id=user_province)
        if user_municipality:
            q &= Q(user__municipality__id=user_municipality)

        candidates = Applicant.objects.filter(q)
    else:
        posting = CompanyJobPosting.objects.get(id=_id)
        candidates = posting.get_candidates

    htmlStr = render_to_string('posting_candidates_list_render.html', {
        'candidates': candidates
    })

    return JsonResponse({
        'success': True,
        'htmlStr': htmlStr,
    })


def ajax_get_invites(request):
    _id = request.GET.get('_id')
    posting = CompanyJobPosting.objects.get(id=_id)
    htmlStr = render_to_string('posting_invites_list_render.html', {
        'posting': posting,
    })

    return JsonResponse({
        'success': True,
        'htmlStr': htmlStr,
    })


def ajax_edit_job_posting(request):

    _id = request.POST.get('id')
    job_title = request.POST.get('job_title')
    description = request.POST.get('description')
    vacancy = request.POST.get('vacancy')
    salary_range_end = request.POST.get('salary_range_end')
    salary_range_start = request.POST.get('salary_range_start')
    preferred_skills = request.POST.get('preferred_skills')
    attachments = request.FILES.getlist('files')

    posting = CompanyJobPosting.objects.get(pk=_id)
    posting.company = request.user.company_data
    posting.job_title = job_title
    posting.description = description
    posting.vacancy = vacancy
    posting.salary_range_end = salary_range_end
    posting.salary_range_start = salary_range_start
    posting.preferred_skills = preferred_skills
    posting.save()

    for file in attachments:
        data = {
            'job_posting': posting,
            'attachment': file,
        }
        JobPostingAttachment.objects.create(**data)

    message = f'''<div class="alert alert-success alert-dismissible fade show" role="alert">Successfully Updated.</div>'''
    postingStr = render_to_string('job_posting_details_page.html', {
        'posting': posting,
        'employment_type_choices': dict(EMPLOYMENT_TYPE_CHOICES),
        'csrf_token': django.middleware.csrf.get_token(request),
        'message': message,
    })

    return JsonResponse({
        'success': True,
        'postingStr': postingStr,
    })


def ajax_add_job_posting(request):

    job_title = request.POST.get('job_title')
    description = request.POST.get('description')
    vacancy = request.POST.get('vacancy')
    salary_range_end = request.POST.get('salary_range_end')
    salary_range_start = request.POST.get('salary_range_start')
    preferred_skills = request.POST.get('preferred_skills')
    attachments = request.FILES.getlist('files')

    data = {
        'company': request.user.company_data,
        'job_title': job_title,
        'description': description,
        'vacancy': vacancy,
        'salary_range_end': salary_range_end,
        'salary_range_start': salary_range_start,
        'preferred_skills': preferred_skills,
    }
    posting = CompanyJobPosting.objects.create(**data)

    for file in attachments:
        data = {
            'job_posting': posting,
            'attachment': file,
        }
        JobPostingAttachment.objects.create(**data)

    postings = request.user.company_data.company_jobs.all().order_by('-created_at').values()
    attachments = posting.job_posting_attachments.all().order_by('-created_at').values()

    postingStr = ''
    for posting in postings:
        postingStr += render_to_string('job_posting_table_item.html', {
            'posting': posting,
        })

    return JsonResponse({
        'success': True,
        'postingStr': postingStr,
        'attachments': list(attachments),
    })


def ajax_job_details(request):
    _id = request.GET.get('id')

    postingStr = render_to_string('job_posting_details_page.html', {
        'posting': CompanyJobPosting.objects.get(id=_id),
        'employment_type_choices': dict(EMPLOYMENT_TYPE_CHOICES),
        'csrf_token': django.middleware.csrf.get_token(request),
        'regions': Region.objects.all(),
        'provinces': Province.objects.all(),
        'municipalities': Municipality.objects.all(),
    })
    return JsonResponse({
        'success': True,
        'postingStr': postingStr,
    })


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
    start_month = datetime.now().strftime("%m")
    start_year = datetime.now().year

    data = {
        'applicant': user.applicant_data,
        'company_name': job_posting.company.name,
        'job_position': job_posting.job_title,
        'employment_type': job_posting.employment_type,
        'start_month': start_month,
        'start_year': start_year,
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

    to_email = user.email
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
    user_id = request.GET.get('user_id')
    action = request.GET.get('action')
    job_posting = CompanyJobPosting.objects.get(id=_id)
    user = CustomUser.objects.get(id=user_id)

    data = {
        'company_job': job_posting,
        'applicant': user.applicant_data,
    }

    if action == 'apply':
        JobPostingApplicant.objects.create(**data)
    else:
        applicants = JobPostingApplicant.objects.filter(**data)
        applicants.delete()

    applicantsStr = ""
    for applicant in job_posting.job_applicants.all():
        applicantsStr += render_to_string('new_applicant_email.html', {
            'job_applicant': request.user,
            'posting': job_posting,
        })

    mail_subject = f'Invitation for position: {job_posting.job_title}'
    message = render_to_string('job_invitation_email.html', {
        'user': user,
        'hiring_agent': job_posting.company.owner,
        'job_posting': job_posting,
        'user_profile': reverse_lazy('users:profile_edit',
                                     kwargs={'pk': user_id})
    })

    to_email = user.email

    send_mail(
        mail_subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email],
        fail_silently=True,
    )

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
