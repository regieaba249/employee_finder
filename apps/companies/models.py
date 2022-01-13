from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.users.models import CustomUser, Applicant
from employee_finder.models import BaseModel


optional = {
    'blank': True,
    'null': True
}

EMPLOYMENT_STATUS_CHOICES = (
    ('full_time', 'Full Time'),
    ('part_time', 'Part Time'),
    ('contract', 'Contractual'),
    ('intern', 'Internship'),
    ('terminated', 'Terminated'),
)

JOB_APPLICANT_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('interview', 'For Interview'),
    ('hired', 'Hired'),
    ('declined', 'Declined'),
)


# Create your models here.
class Company(BaseModel):
    owner = models.OneToOneField(
        CustomUser,
        related_name='company_data',
        on_delete=models.CASCADE,
        unique=True,
        **optional
    )
    name = models.CharField(max_length=250, **optional)
    founded_on = models.DateField(**optional)
    website = models.CharField(max_length=100, **optional)
    overview = models.TextField(**optional)
    employee_count = models.IntegerField(**optional)
    email = models.EmailField(_('Email Address'), unique=True)
    phone_number = models.CharField(max_length=10, **optional)
    mobile_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Mobile number format must be: '+639999999999'.")
    mobile_number = models.CharField(validators=[mobile_regex], max_length=13, **optional) # validators should be a list

    def __str__(self):
        return f"{self.owner.full_name} {self.owner.email}"


class CompanyJob(BaseModel):
    company = models.ForeignKey(
        Company,
        related_name='company_jobs',
        on_delete=models.CASCADE,
        null=True
    )
    job_title = models.CharField(max_length=250, **optional)
    description = models.TextField(**optional)
    vacancy = models.IntegerField(**optional)
    salary_range_end = models.DecimalField(max_digits=6, decimal_places=2)
    salary_range_start = models.DecimalField(max_digits=6, decimal_places=2)


class CompanyJobApplicant(BaseModel):
    company_job = models.ForeignKey(
        CompanyJob,
        related_name='company_jobs',
        on_delete=models.CASCADE,
        null=True
    )
    applicant = models.ForeignKey(
        Applicant,
        related_name='company_jobs',
        on_delete=models.CASCADE,
        null=True
    )
    status = models.CharField(
        max_length=10,
        choices=JOB_APPLICANT_STATUS_CHOICES,
        default='pending'
    )


class CompanyEmployee(BaseModel):
    applicant = models.ForeignKey(
        Applicant,
        related_name='company_employees',
        on_delete=models.CASCADE,
        null=True
    )
    hire_date = models.DateField(**optional)
    job_title = models.CharField(max_length=250, **optional)
    salary = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=EMPLOYMENT_STATUS_CHOICES,
        default='full_time'
    )
