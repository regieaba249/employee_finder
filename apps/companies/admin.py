from django.contrib import admin
from apps.companies.models import (
    Company,
    CompanyJob,
    CompanyEmployee,
)


@admin.register(Company)
class Company(admin.ModelAdmin):
    search_fields = ('__all__',)


@admin.register(CompanyJob)
class CompanyJob(admin.ModelAdmin):
    search_fields = ('__all__',)


@admin.register(CompanyEmployee)
class CompanyEmployee(admin.ModelAdmin):
    search_fields = ('__all__',)
