# Generated by Django 4.0 on 2022-01-29 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_alter_usersubscription_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usersubscription',
            old_name='_type',
            new_name='payment_type',
        ),
    ]
