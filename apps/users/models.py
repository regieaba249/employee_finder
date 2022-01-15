from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from employee_finder.managers import CustomUserManager

from employee_finder.models import BaseModel


optional = {
    'blank': True,
    'null': True
}

EFFICIENCY_CHOICES = (
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
)

MONTH_CHOICES = (
    ('', '------'),
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
    ('dec', 'December')
)

GENDER_CHOICES = (
    ('select', 'Select...'),
    ('male', 'Male'),
    ('female', 'Female'),
    ('others', 'Others')
)

USER_TYPE_CHOICES = (
    ('employer', 'Employer'),
    ('applicant', 'Applicant')
)

APPLICANT_STATUS_CHOICES = (
    ('employed', 'Employed'),
    ('unemployed', 'Unemployed')
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
    mobile_number = models.CharField(validators=[mobile_regex], max_length=13, **optional) # validators should be a list
    headline = models.CharField(max_length=250, **optional)
    birthdate = models.DateField(**optional)
    user_avatar = models.ImageField(default='user_avatar.png', upload_to='user_avatars', **optional)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='select',
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
    resume = models.FileField(**optional)
    overview = models.TextField(**optional)
    # minimum_expected_salary

    def __str__(self):
        return f"{self.user.email}"

    def delete(self, using=None, keep_parents=False):
        self.resume.storage.delete(self.resume.name)
        super().delete()


class ApplicantAttachment(BaseModel):
    applicant = models.ForeignKey(
        Applicant,
        related_name='applicant_attachments',
        on_delete=models.CASCADE,
        null=True
    )
    attachment = models.FileField(null=True)

    def __str__(self):
        return f"{self.attachment}"

    def delete(self, using=None, keep_parents=False):
        self.attachment.storage.delete(self.attachment.name)
        super().delete()


class ApplicantExperience(BaseModel):
    applicant = models.ForeignKey(
        Applicant,
        related_name='applicant_experience',
        on_delete=models.CASCADE,
        null=True
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
        default='select',
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
        return f"{self.applicant.user.email}"

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
    name = models.FileField(**optional)
    efficiency = models.CharField(
        max_length=12,
        choices=EFFICIENCY_CHOICES,
        default='1'
    )
    attachment = models.FileField(null=True)

    def __str__(self):
        return f"{self.applicant.user.email}"


class ApplicantSeminar(BaseModel):
    applicant = models.ForeignKey(
        Applicant,
        related_name='applicant_seminars',
        on_delete=models.CASCADE,
        null=True
    )
    summary = models.FileField(**optional)
    description = models.TextField(**optional)
    birthdate = models.DateField(**optional)

    def __str__(self):
        return f"{self.applicant.user.email}"


class ApplicantSeminarAttachment(BaseModel):
    seminar = models.ForeignKey(
        ApplicantSeminar,
        related_name='seminar_attachments',
        on_delete=models.CASCADE,
        null=True
    )
    attachment = models.FileField(null=True)

    def __str__(self):
        return f"{self.applicant.user.email} - {self.attachment}"