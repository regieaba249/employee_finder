# Generated by Django 4.0 on 2022-01-13 00:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0008_alter_companyjob_salary_range_end_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyJobPosting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('job_title', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, null=True)),
                ('vacancy', models.IntegerField(blank=True, null=True)),
                ('salary_range_end', models.DecimalField(decimal_places=2, max_digits=10)),
                ('salary_range_start', models.DecimalField(decimal_places=2, max_digits=10)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_jobs', to='companies.company')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='companyjobapplicant',
            name='company_job',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_jobs', to='companies.companyjobposting'),
        ),
        migrations.DeleteModel(
            name='CompanyJob',
        ),
    ]