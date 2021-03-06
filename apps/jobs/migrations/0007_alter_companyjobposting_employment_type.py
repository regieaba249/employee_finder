# Generated by Django 4.0 on 2022-01-16 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_companyjobposting_preferred_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyjobposting',
            name='employment_type',
            field=models.CharField(choices=[('full_time', 'Full Time'), ('part_time', 'Part Time'), ('self_employed', 'Self Employed'), ('freelance', 'Freelance'), ('contract', 'Contractual'), ('internship', 'Internship')], default='full_time', max_length=15),
        ),
    ]
