# Generated by Django 4.0 on 2022-01-09 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('address', models.CharField(blank=True, max_length=250, null=True)),
                ('founded_on', models.DateField(blank=True, null=True)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
                ('overview', models.TextField(blank=True, null=True)),
                ('employee_count', models.IntegerField(blank=True, null=True)),
                ('company_avatar', models.ImageField(blank=True, default='company_avatar.png', null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyEmployee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hire_date', models.DateField(blank=True, null=True)),
                ('job_title', models.CharField(blank=True, max_length=250, null=True)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=6)),
                ('status', models.CharField(choices=[('full_time', 'Full Time'), ('part_time', 'Part Time'), ('contract', 'Contractual'), ('intern', 'Internship'), ('terminated', 'Terminated')], default='full_time', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(blank=True, max_length=250, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('vacancy', models.IntegerField(blank=True, null=True)),
                ('salary_range_end', models.DecimalField(decimal_places=2, max_digits=6)),
                ('salary_range_start', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
    ]
