# Generated by Django 4.0 on 2022-01-25 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_alter_customuser_mobile_number_applicantproject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicanteducation',
            name='end_month',
            field=models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=1),
        ),
        migrations.AlterField(
            model_name='applicanteducation',
            name='start_month',
            field=models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=1),
        ),
        migrations.AlterField(
            model_name='applicantexperience',
            name='end_month',
            field=models.IntegerField(blank=True, choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=1, null=True),
        ),
        migrations.AlterField(
            model_name='applicantexperience',
            name='start_month',
            field=models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=1),
        ),
        migrations.AlterField(
            model_name='applicantproject',
            name='end_month',
            field=models.IntegerField(blank=True, choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=1, null=True),
        ),
        migrations.AlterField(
            model_name='applicantproject',
            name='start_month',
            field=models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=1),
        ),
    ]
