# Generated by Django 4.0 on 2022-01-16 15:42

from django.db import migrations, models
import employee_finder.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_applicant_resume_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicantattachment',
            name='attachment',
            field=models.FileField(upload_to=employee_finder.helpers.get_upload_to),
        ),
    ]