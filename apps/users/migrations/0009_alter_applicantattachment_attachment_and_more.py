# Generated by Django 4.0 on 2022-01-13 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_applicant_is_active_applicantattachment_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicantattachment',
            name='attachment',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='applicantseminarattachment',
            name='attachment',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
