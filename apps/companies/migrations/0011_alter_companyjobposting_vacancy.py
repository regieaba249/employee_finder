# Generated by Django 4.0 on 2022-01-13 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0010_company_is_active_companyemployee_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyjobposting',
            name='vacancy',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
