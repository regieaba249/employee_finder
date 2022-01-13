from django.contrib import admin
from .models import JobPostingApplicant


# Register your models here.
@admin.register(JobPostingApplicant)
class JobPostingApplicant(admin.ModelAdmin):
    search_fields = ('__all__',)
