import re

from django.db import models
from django.db.models import Q

from functools import reduce

from apps.companies.models import (
    Company
)
from apps.users.models import (
    Applicant,
    ApplicantSkill
)
from employee_finder.models import BaseModel
from employee_finder.helpers import (
    # functions
    get_upload_to,

    # reusable values
    optional,
    EMPLOYMENT_TYPE_CHOICES
)


JOB_APPLICANT_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('interview', 'For Interview'),
    ('hired', 'Hired'),
    ('declined', 'Declined'),
)


# Create your models here.
class CompanyJobPosting(BaseModel):
    company = models.ForeignKey(
        Company,
        related_name='company_jobs',
        on_delete=models.CASCADE,
        null=True
    )
    job_title = models.CharField(max_length=250)
    description = models.TextField(**optional)
    vacancy = models.IntegerField(default=1, **optional)
    salary_range_start = models.DecimalField(max_digits=10, decimal_places=2)
    salary_range_end = models.DecimalField(max_digits=10, decimal_places=2)
    employment_type = models.CharField(
        max_length=15,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default='full_time'
    )
    preferred_skills = models.CharField(max_length=255, **optional)

    def __str__(self):
        return f"{self.company.name} - {self.job_title}"

    @property
    def salary_range(self):
        return f'{self.salary_range_end} - {self.salary_range_start}'

    @property
    def get_applicants(self):
        return [x.applicant for x in self.job_applicants.all()]

    @property
    def get_declined(self):
        return [x.applicant for x in self.job_applicants.filter(status='declined')]

    @property
    def get_candidates(self):
        preferred_skills = re.split(', |,', self.preferred_skills)
        applicant_ids = ApplicantSkill.objects.filter(
            reduce(lambda x, y: x | y, [
                Q(name__contains=word) for word in preferred_skills
            ])
        ).values_list('applicant', flat=True)
        picked_ids = self.job_applicants.all().values_list('applicant__id', flat=True)
        queryset = Applicant.objects.filter(id__in=applicant_ids).exclude(id__in=picked_ids)
        return sorted(queryset, key=lambda t: t.get_total_points, reverse=True)


class JobPostingAttachment(BaseModel):
    job_posting = models.ForeignKey(
        CompanyJobPosting,
        related_name='job_posting_attachments',
        on_delete=models.CASCADE,
        null=True
    )
    attachment = models.FileField(upload_to=get_upload_to, null=True)

    def __str__(self):
        return f"{self.job_posting}"

    def delete(self, using=None, keep_parents=False):
        self.attachment.storage.delete(self.attachment.name)
        super().delete()

    @property
    def get_user_id(self):
        return self.job_posting.company.owner.id


class JobPostingApplicant(BaseModel):
    company_job = models.ForeignKey(
        CompanyJobPosting,
        related_name='job_applicants',
        on_delete=models.CASCADE,
        null=True
    )
    applicant = models.ForeignKey(
        Applicant,
        related_name='job_applicants',
        on_delete=models.CASCADE,
        null=True
    )
    status = models.CharField(
        max_length=10,
        choices=JOB_APPLICANT_STATUS_CHOICES,
        default='pending'
    )
