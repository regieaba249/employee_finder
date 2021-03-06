# Generated by Django 4.0 on 2022-01-16 15:01

from django.db import migrations, models
import employee_finder.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_applicanteducation_end_month_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to=employee_finder.helpers.get_upload_to),
        ),
        migrations.AlterField(
            model_name='applicantattachment',
            name='attachment',
            field=models.FileField(default=2, upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='applicantskill',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
