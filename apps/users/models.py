from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


optional = {
    'blank': True,
    'null': True
}

EFFICIENCY_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
)

MONTH_CHOICES = (
    ('select', 'Select...'),
    ('jan', 'January'),
    ('feb', 'February'),
    ('mar', 'March'),
    ('apr', 'April'),
    ('may', 'May'),
    ('jun', 'June'),
    ('jul', 'July'),
    ('aug', 'August'),
    ('sep', 'September'),
    ('oct', 'October'),
    ('nov', 'November'),
    ('dec', 'December'),
)

GENDER_CHOICES = (
    ('select', 'Select...'),
    ('male', 'Male'),
    ('female', 'Female'),
    ('others', 'Others'),
)

USER_TYPE_CHOICES = (
    ('employer', 'Employer'),
    ('applicant', 'Applicant'),
)

APPLICANT_STATUS_CHOICES = (
    ('employed', 'Employed'),
    ('unemployed', 'Unemployed'),
)

EMPLOYMENT_TYPE_CHOICES = (
    ('select', 'Select...'),
    ('full_time', 'Full Time'),
    ('part_time', 'Part Time'),
    ('self_employed', 'Self Employed'),
    ('freelance', 'Freelance'),
    ('contract', 'Contractual'),
    ('internship', 'Internship'),
)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    middle_name = models.CharField(max_length=50, **optional)
    extension = models.CharField(max_length=50, **optional)
    address = models.CharField(max_length=250, **optional)
    email = models.EmailField(_('Email Address'), unique=True)
    phone_number = models.CharField(max_length=10, **optional)
    mobile_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Mobile number format must be: '+639999999999'.")
    mobile_number = models.CharField(validators=[mobile_regex], max_length=13, **optional) # validators should be a list
    headline = models.CharField(max_length=250, **optional)
    birthdate = models.DateField(**optional)
    user_avatar = models.ImageField(default='user_avatar.png', upload_to='user_avatars', **optional)
    overview = models.TextField(**optional)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='select'
    )
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='applicant',
        **optional
    )
    token = models.CharField(max_length=250, **optional)
    is_superadmin = models.BooleanField(_('is_superadmin'), default=False)
    is_active = models.BooleanField(_('is_active'), default=False)
    is_staff = models.BooleanField(default=True)
    # followers
    # following

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'middle_name',
    ]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name} {self.middle_name} {self.extension if self.extension else ''}"

    @property
    def contact_numbers(self):
        if self.phone_number and self.mobile_number:
            numbers = f"{self.phone_number} | {self.mobile_number}"
        elif self.phone_number:
            numbers = self.phone_number
        elif self.mobile_number:
            numbers = self.mobile_number
        else:
            numbers = ""
        return numbers


class Applicant(models.Model):
    user = models.OneToOneField(
        CustomUser,
        related_name='applicant_data',
        on_delete=models.CASCADE,
        unique=True,
        **optional
    )
    applicant_status = models.CharField(
        max_length=10,
        choices=APPLICANT_STATUS_CHOICES,
        default='unemployed'
    )
    resume = models.FileField(**optional)
    # minimum_expected_salary

    def __str__(self):
        return f"{self.user.email}"


class ApplicantAttachments(models.Model):
    applicant = models.ForeignKey(
        Applicant,
        related_name='applicant_attachments',
        on_delete=models.CASCADE
    )
    attachment = models.FileField(**optional)

    def __str__(self):
        return f"{self.applicant.user.email} - {self.attachment}"


class ApplicantExperience(models.Model):
    applicant = models.ForeignKey(
        Applicant,
        related_name='applicant_experience',
        on_delete=models.CASCADE
    )
    company_name = models.CharField(max_length=50, blank=False)
    start_month = models.CharField(
        max_length=15,
        choices=MONTH_CHOICES,
        default='select'
    )
    start_year = models.CharField(max_length=50, blank=False)
    end_month = models.CharField(
        max_length=15,
        choices=MONTH_CHOICES,
        default='select'
    )
    end_year = models.CharField(max_length=50, blank=False)
    job_position = models.CharField(max_length=100, blank=False)
    employment_type = models.CharField(
        max_length=15,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default='select'
    )
    current = models.BooleanField(default=False)
    description = models.TextField(**optional)

    def __str__(self):
        return f"{self.applicant.user.email}"


class ApplicantEducation(models.Model):
    applicant = models.ForeignKey(
        Applicant,
        related_name='applicant_education',
        on_delete=models.CASCADE
    )
    school = models.CharField(max_length=250, blank=False)
    degree = models.CharField(max_length=250, blank=False)
    start_month = models.CharField(
        max_length=15,
        choices=MONTH_CHOICES,
        default='select'
    )
    start_year = models.CharField(max_length=50, blank=False)
    end_month = models.CharField(
        max_length=15,
        choices=MONTH_CHOICES,
        default='select'
    )
    end_year = models.CharField(max_length=50, blank=False)
    description = models.TextField(**optional)

    def __str__(self):
        return f"{self.applicant.user.email}"


class ApplicantSkills(models.Model):
    applicant = models.ForeignKey(
        Applicant,
        related_name='applicant_skills',
        on_delete=models.CASCADE
    )
    name = models.FileField(**optional)
    efficiency = models.CharField(
        max_length=2,
        choices=EFFICIENCY_CHOICES,
        default='1'
    )

    def __str__(self):
        return f"{self.applicant.user.email}"


class ApplicantSeminars(models.Model):
    applicant = models.ForeignKey(
        Applicant,
        related_name='applicant_seminars',
        on_delete=models.CASCADE
    )
    summary = models.FileField(**optional)
    description = models.TextField(**optional)
    birthdate = models.DateField(**optional)

    def __str__(self):
        return f"{self.applicant.user.email}"


class ApplicantSeminarsAttachments(models.Model):
    seminar = models.ForeignKey(
        ApplicantSeminars,
        related_name='seminar_attachments',
        on_delete=models.CASCADE
    )
    attachment = models.FileField(**optional)

    def __str__(self):
        return f"{self.applicant.user.email} - {self.attachment}"