# Generated by Django 4.0 on 2022-01-30 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_alter_usersubscription_expiry_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersubscription',
            name='is_current',
            field=models.BooleanField(default=True, verbose_name='is_current'),
        ),
        migrations.AlterField(
            model_name='usersubscription',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]