from django.db import models
from apps.companies.models import (
    Company
)
from apps.users.models import (
    Applicant
)
from employee_finder.models import BaseModel

optional = {
    'blank': True,
    'null': True
}

JOB_APPLICANT_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('interview', 'For Interview'),
    ('hired', 'Hired'),
    ('declined', 'Declined'),
)
EMPLOYMENT_TYPE_CHOICES = (
    ('select', 'Select...'),
    ('full_time', 'Full Time'),
    ('part_time', 'Part Time'),
    ('self_employed', 'Self Employed'),
    ('freelance', 'Freelance'),
    ('contract', 'Contractual'),
    ('internship', 'Internship')
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


class JobPostingAttachment(BaseModel):
    job_posting = models.ForeignKey(
        CompanyJobPosting,
        related_name='job_posting_attachments',
        on_delete=models.CASCADE,
        null=True
    )
    attachment = models.FileField(null=True)

    def __str__(self):
        return f"{self.job_posting}"

    def delete(self, using=None, keep_parents=False):
        self.attachment.storage.delete(self.attachment.name)
        super().delete()


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
