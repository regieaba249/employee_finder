from django.contrib import admin
from apps.companies.models import (
    Company,
    CompanyEmployee
)
from apps.jobs.models import (
    CompanyJobPosting,
    JobPostingAttachment
)


@admin.register(Company)
class Company(admin.ModelAdmin):
    search_fields = ('__all__',)


@admin.register(CompanyJobPosting)
class CompanyJobPosting(admin.ModelAdmin):
    search_fields = ('__all__',)


@admin.register(JobPostingAttachment)
class JobPostingAttachment(admin.ModelAdmin):
    search_fields = ('__all__',)


@admin.register(CompanyEmployee)
class CompanyEmployee(admin.ModelAdmin):
    search_fields = ('__all__',)
