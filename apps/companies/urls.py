from django.urls import path, re_path
from . import views

app_name = 'apps.companies'
urlpatterns = [
    path('profile/edit/<int:pk>/', views.CompanyUpdateView.as_view(), name='profile_edit'),
    path('ajax/add-job-posting/', views.ajax_add_job_posting, name='ajax_add_job_posting'),
]
