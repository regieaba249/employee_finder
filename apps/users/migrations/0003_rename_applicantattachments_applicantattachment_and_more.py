# Generated by Django 4.0 on 2022-01-11 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_applicantexperience_mobile_number_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ApplicantAttachments',
            new_name='ApplicantAttachment',
        ),
        migrations.RenameModel(
            old_name='ApplicantSeminars',
            new_name='ApplicantSeminar',
        ),
        migrations.RenameModel(
            old_name='ApplicantSeminarsAttachments',
            new_name='ApplicantSeminarAttachment',
        ),
        migrations.RenameModel(
            old_name='ApplicantSkills',
            new_name='ApplicantSkill',
        ),
    ]
