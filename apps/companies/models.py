from django.db import models

from apps.users.models import CustomUser, Applicant


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


# Create your models here.
class Company(models.Model):
    owner = models.OneToOneField(
        CustomUser,
        related_name='company_data',
        on_delete=models.CASCADE,
        unique=True,
        **optional
    )
    name = models.CharField(max_length=250, **optional)
    address = models.CharField(max_length=250, **optional)
    founded_on = models.DateField(**optional)
    website = models.CharField(max_length=100, **optional)
    overview = models.TextField(**optional)
    employee_count = models.IntegerField(**optional)
    company_avatar = models.ImageField(default='company_avatar.png', **optional)

    def __str__(self):
        return f"{self.owner.full_name} {self.owner.email}"


class CompanyJob(models.Model):
    job_title = models.CharField(max_length=250, **optional)
    description = models.TextField(**optional)
    vacancy = models.IntegerField(**optional)
    salary_range_end = models.DecimalField(max_digits=6, decimal_places=2)
    salary_range_start = models.DecimalField(max_digits=6, decimal_places=2)


class CompanyEmployee(models.Model):
    applicant = models.ForeignKey(
        Applicant,
        related_name='company_employees',
        on_delete=models.CASCADE
    )
    hire_date = models.DateField(**optional)
    job_title = models.CharField(max_length=250, **optional)
    salary = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=EMPLOYMENT_STATUS_CHOICES,
        default='full_time'
    )
