optional = {
    'blank': True,
    'null': True
}

SUBSCRIPTION_TYPE = (
    ('monthly', 'Monthly'),
    ('semi', 'Semi-annually'),
    ('annually', 'Annually'),
)

EFFICIENCY_CHOICES = (
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
)

MONTH_CHOICES = (
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
    ('full_time', 'Full Time'),
    ('part_time', 'Part Time'),
    ('self_employed', 'Self Employed'),
    ('freelance', 'Freelance'),
    ('contract', 'Contractual'),
    ('internship', 'Internship')
)

def get_upload_to(instance, filename):
    model_name = instance._meta.model.__name__
    user_id = instance.get_user_id
    return f'{model_name}/user_{user_id}/{filename}'
