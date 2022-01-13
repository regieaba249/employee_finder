# Generated by Django 4.0 on 2022-01-13 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0009_companyjobposting_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='companyemployee',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='companyjobapplicant',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='companyjobposting',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
