# Generated by Django 4.0 on 2021-12-14 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_company_company_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='address',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
