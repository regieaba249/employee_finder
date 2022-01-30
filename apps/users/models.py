import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from employee_finder.managers import CustomUserManager

from employee_finder.models import BaseModel
from employee_finder.helpers import (
    # functions
    get_upload_to,

    # reusable values
    optional,
    EFFICIENCY_CHOICES,
    MONTH_CHOICES,
    GENDER_CHOICES,
    USER_TYPE_CHOICES,
    APPLICANT_STATUS_CHOICES,
    EMPLOYMENT_TYPE_CHOICES
)


class AreaCode(BaseModel):
    code = models.CharField(max_length=5, blank=False)
    name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Region(BaseModel):
    ISLAND_GROUP_LUZON = 'L'
    ISLAND_GROUP_VISAYAS = 'V'
    ISLAND_GROUP_MINDANAO = 'M'
    ISLAND_GROUP_CHOICES = (
        (ISLAND_GROUP_LUZON, 'LUZON'),
        (ISLAND_GROUP_VISAYAS, 'VISAYAS'),
        (ISLAND_GROUP_MINDANAO, 'MINDANAO'),
    )
    name = models.CharField(max_length=100, null=False, verbose_name='Name')
    island_group = models.CharField(max_length=1, choices=ISLAND_GROUP_CHOICES,
                                    null=False, verbose_name='Island Group')

    def __str__(self):
        return f"{self.name}"


class Province(BaseModel):
    name = models.CharField(max_length=100, null=False, verbose_name='Name')
    region = models.ForeignKey(
        Region,
        related_name='provinces',
        related_query_name='province',
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Region'
    )

    def __str__(self):
        return f"{self.name}"


class Municipality(BaseModel):
    name = models.CharField(max_length=100, null=False, verbose_name='Name')
    province = models.ForeignKey(
        Province,
        related_name='municipalities',
        related_query_name='municipality',
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Province'
    )

    def __str__(self):
        return f"{self.name}"


class Barangay(BaseModel):
    name = models.CharField(max_length=100, null=False, verbose_name='Name')
    municipality = models.ForeignKey(
        Municipality,
        related_name='barangays',
        related_query_name='barangays',
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Barangay'
    )

    def __str__(self):
        return f"{self.name}"


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    middle_name = models.CharField(max_length=50, **optional)
    extension = models.CharField(max_length=50, **optional)
    email = models.EmailField(_('Email Address'), unique=True)
    area_code = models.CharField(max_length=5, **optional)
    phone_number = models.CharField(max_length=10, **optional)
    mobile_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Mobile number format must be: '+639999999999'.")
    mobile_number = models.CharField(validators=[mobile_regex], max_length=13, blank=False)
    headline = models.CharField(max_length=250, **optional)
    birthdate = models.DateField(**optional)
    user_avatar = models.ImageField(default='user_avatar.png', upload_to='user_avatars', **optional)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        **optional
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
    is_paid = models.BooleanField(default=False)
    address = models.CharField(max_length=250, **optional)
    region = models.ForeignKey(
        Region,
        related_name='region_users',
        on_delete=models.CASCADE,
        null=True
    )
    province = models.ForeignKey(
        Province,
        related_name='province_users',
        on_delete=models.CASCADE,
        null=True
    )
    municipality = models.ForeignKey(
        Municipality,
        related_name='municipality_users',
        on_delete=models.CASCADE,
        null=True
    )
    barangay = models.ForeignKey(
        Barangay,
        related_name='barangay_users',
        on_delete=models.CASCADE,
        null=True
    )
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
        return f"{self.email} ({self.user_type})"

    def __unicode__(self):
        return self.email

    @property
    def get_first_name(self):
        return self.first_name if self.first_name else ''

    @property
    def get_last_name(self):
        return self.last_name if self.last_name else ''

    @property
    def get_middle_name(self):
        return self.middle_name if self.middle_name else ''

    @property
    def get_extension(self):
        return self.extension if self.extension else ''

    @property
    def full_name(self):
        return f"{self.get_first_name} {self.get_last_name} {self.get_middle_name} {self.get_extension}"

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

    @property
    def current_subscription(self):
        user = CustomUser.objects.get(id=self.id)
        current = user.subscriptions.filter(is_active=True).first()
        return current


class Applicant(BaseModel):
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
    resume = models.FileField(upload_to=get_upload_to, **optional)
    overview = models.TextField(**optional)
    # minimum_expected_salary

    def __str__(self):
        return f"{self.user.email}"

    def delete(self, using=None, keep_parents=False):
        self.resume.storage.delete(self.resume.name)
        super().delete()

    @property
    def get_user_id(self):
        return self.user.id

    @property
    def get_total_points(self):
        points = 0
        user = self.user
        points += 1 if user.first_name else 0
        points += 1 if user.last_name else 0
        points += 1 if user.extension else 0
        points += 1 if user.email else 0
        points += 2 if user.phone_number else 0
        points += 2 if user.mobile_number else 0
        points += 5 if user.headline else 0
        points += 1 if user.birthdate else 0
        points += 10 if user.user_avatar else 0
        points += 1 if user.gender else 0
        points += 5 if user.address else 0
        points += 5 if user.region else 0
        points += 5 if user.province else 0
        points += 5 if user.municipality else 0
        points += 5 if user.barangay else 0
        points += 20 if self.resume else 0
        points += 50 if self.overview else 0
        points += self.applicant_attachments.count() * 10
        points += self.applicant_education.count() * 10

        for x in self.applicant_experience.all():
            points += 1 if x.company_name else 0
            points += 1 if x.job_position else 0
            points += 1 if x.employment_type else 0
            points += 10 if x.description else 0
            points += 5 if x.reference_person else 0
            points += 5 if x.mobile_number else 0

        for x in self.applicant_skills.all():
            points += 1 if x.name else 0
            points += 5 if x.attachment else 0
            points += 10 if x.efficiency == "beginner" else 0
            points += 20 if x.efficiency == "intermediate" else 0
            points += 30 if x.efficiency == "advanced" else 0

        return points

    @property
    def get_years_experience(self):
        first = self.applicant_experience.order_by('start_year').first()
        start_date = datetime.strptime(f"01/{first.start_month:02}/{first.start_year}", '%d/%m/%Y')

        last = self.applicant_experience.order_by('-end_year').first()
        end_date = datetime.strptime(f"01/{last.end_month:02}/{last.end_year}", '%d/%m/%Y')

        current = self.applicant_experience.filter(current=True)[0]
        if current:
            end_date = datetime.today()

        return relativedelta(end_date, start_date).years


class ApplicantAttachment(BaseModel):
    applicant = models.ForeignKey(
        Applicant,
        related_name='applicant_attachments',
        on_delete=models.CASCADE,
        null=True
    )
    attachment = models.FileField(upload_to=get_upload_to, null=False)

    def __str__(self):
        return f"{self.attachment}"

    def delete(self, using=None, keep_parents=False):
        self.attachment.storage.delete(self.attachment.name)
        super().delete()

    @property
    def get_user_id(self):
        return self.applicant.user.id

    @property
    def filename(self):
        return os.path.basename(self.attachment.name)


class ApplicantExperience(BaseModel):
    applicant = models.ForeignKey(
        Applicant,
        related_name='applicant_experience',
        on_delete=models.CASCADE,
        null=True
    )
    company_name = models.CharField(max_length=50, blank=False)
    start_month = models.IntegerField(
        choices=MONTH_CHOICES,
        default=1
    )
    start_year = models.CharField(max_length=50, blank=False)
    end_month = models.IntegerField(
        choices=MONTH_CHOICES,
        default=1,
        **optional
    )
    end_year = models.CharField(max_length=50, **optional)
    job_position = models.CharField(max_length=100, blank=False)
    employment_type = models.CharField(
        max_length=15,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default='select'
    )
    current = models.BooleanField(default=False)
    description = models.TextField(**optional)
    reference_person = models.CharField(max_length=250, **optional)
    mobile_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Mobile number format must be: '+639999999999'.")
    mobile_number = models.CharField(validators=[mobile_regex], max_length=13, **optional) # validators should be a list

    def __str__(self):
        return f"{self.applicant.user.email} - {self.company_name}"

    @property
    def start(self):
        if self.start_month and self.start_year:
            months = dict(MONTH_CHOICES)
            return f'{months[self.start_month]} / {self.start_year}'
        return ''

    @property
    def end(self):
        if self.end_month and self.end_year:
            months = dict(MONTH_CHOICES)
            return f'{months[self.end_month]} / {self.end_year}'
        return ''

    @property
    def start_date(self):
        return datetime.strptime(f"01/{self.start_month:02}/{self.start_year}", '%d/%m/%Y')

    @property
    def end_date(self):
        if self.start_month and self.start_year:
            return datetime.strptime(f"01/{self.start_month:02}/{self.start_year}", '%d/%m/%Y')
        return None

    @property
    def full_reference(self):
        if self.reference_person and self.mobile_number:
            ref = f'{self.reference_person} ({self.mobile_number})'
        elif self.reference_person:
            ref = self.reference_person
        else:
            ref = self.mobile_number

        return ref

    def save(self, *args, **kwargs):
        res = ApplicantExperience.objects.filter(applicant=self.applicant, current=True)
        res.update(current=False)
        super(ApplicantExperience, self).save(*args, **kwargs)


class ApplicantEducation(BaseModel):
    applicant = models.ForeignKey(
        Applicant,
        related_name='applicant_education',
        on_delete=models.CASCADE,
        null=True
    )
    school_name = models.CharField(max_length=250, blank=False)
    degree = models.CharField(max_length=250, **optional)
    start_month = models.IntegerField(
        choices=MONTH_CHOICES,
        default=1
    )
    start_year = models.CharField(max_length=50, blank=False)
    end_month = models.IntegerField(
        choices=MONTH_CHOICES,
        default=1
    )
    end_year = models.CharField(max_length=50, blank=False)
    reference_person = models.CharField(max_length=250, **optional)
    mobile_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Mobile number format must be: '+639999999999'.")
    mobile_number = models.CharField(validators=[mobile_regex], max_length=13, **optional) # validators should be a list

    def __str__(self):
        return f"{self.applicant.user.email} - ({self.school_name})"

    @property
    def start(self):
        if self.start_month and self.start_year:
            months = dict(MONTH_CHOICES)
            return f'{months[self.start_month]} / {self.start_year}'
        return ''

    @property
    def end(self):
        if self.end_month and self.end_year:
            months = dict(MONTH_CHOICES)
            return f'{months[self.end_month]} / {self.end_year}'
        return ''

    @property
    def full_reference(self):
        if self.reference_person and self.mobile_number:
            ref = f'{self.reference_person} ({self.mobile_number})'
        elif self.reference_person:
            ref = self.reference_person
        else:
            ref = self.mobile_number

        return ref


class ApplicantSkill(BaseModel):
    applicant = models.ForeignKey(
        Applicant,
        related_name='applicant_skills',
        on_delete=models.CASCADE,
        null=True
    )
    name = models.CharField(max_length=50, blank=False)
    efficiency = models.CharField(
        max_length=12,
        choices=EFFICIENCY_CHOICES,
        default='beginner'
    )
    attachment = models.FileField(upload_to=get_upload_to, **optional)

    def __str__(self):
        return f"{self.applicant.user.email}"

    @property
    def get_user_id(self):
        return self.applicant.user.id


class ApplicantProject(BaseModel):
    experience = models.ForeignKey(
        ApplicantExperience,
        related_name='projects',
        on_delete=models.CASCADE,
        null=True
    )
    title = models.CharField(max_length=50, blank=False)
    start_month = models.IntegerField(
        choices=MONTH_CHOICES,
        default=1
    )
    start_year = models.CharField(max_length=50, blank=False)
    end_month = models.IntegerField(
        choices=MONTH_CHOICES,
        default=1,
        **optional
    )
    end_year = models.CharField(max_length=50, **optional)
    overview = models.TextField(**optional)

    def __str__(self):
        return f"{self.applicant.user.full_name} - {self.title}"

    @property
    def start(self):
        if self.start_month and self.start_year:
            months = dict(MONTH_CHOICES)
            return f'{months[self.start_month]} / {self.start_year}'
        return ''

    @property
    def end(self):
        if self.end_month and self.end_year:
            months = dict(MONTH_CHOICES)
            return f'{months[self.end_month]} / {self.end_year}'
        return ''


class ApplicantSeminar(BaseModel):
    applicant = models.ForeignKey(
        Applicant,
        related_name='applicant_seminars',
        on_delete=models.CASCADE,
        null=True
    )
    summary = models.FileField(upload_to=get_upload_to, **optional)
    description = models.TextField(**optional)
    birthdate = models.DateField(**optional)

    def __str__(self):
        return f"{self.applicant.user.email}"

    @property
    def get_user_id(self):
        return self.applicant.user.id


class ApplicantSeminarAttachment(BaseModel):
    seminar = models.ForeignKey(
        ApplicantSeminar,
        related_name='seminar_attachments',
        on_delete=models.CASCADE,
        null=True
    )
    attachment = models.FileField(upload_to=get_upload_to, null=True)

    def __str__(self):
        return f"{self.applicant.user.email} - {self.attachment}"

    @property
    def get_user_id(self):
        return self.seminar.applicant.user.id
