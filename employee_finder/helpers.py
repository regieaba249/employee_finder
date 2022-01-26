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
    (1, 'January'),
    (2, 'February'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'August'),
    (9, 'September'),
    (10, 'October'),
    (11, 'November'),
    (12, 'December')
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

AREA_CODES = ['02', '032', '033', '034', '035', '036',
              '038', '042', '043', '044', '045', '046',
              '047', '048', '049', '052', '053', '054',
              '055', '056', '062', '063', '064', '065',
              '068', '072', '074', '075', '077', '078',
              '082', '083', '084', '085', '086', '087',
              '088', '08822', '08842']

JOB_APPLICANT_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('interview', 'For Interview'),
    ('hired', 'Hired'),
    ('declined', 'Declined'),
)


def get_upload_to(instance, filename):
    model_name = instance._meta.model.__name__
    user_id = instance.get_user_id
    return f'{model_name}/user_{user_id}/{filename}'
