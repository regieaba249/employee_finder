from django.urls import path
from . import views

app_name = 'apps.jobs'
urlpatterns = [
    path('board/', views.JobsBoardView.as_view(), name='jobs-board'),
    path('ajax/apply/', views.ajax_apply, name='ajax_apply'),
    path('ajax/schedule_interview/', views.ajax_schedule_interview, name='ajax_schedule_interview'),
    path('ajax/decline_applicant/', views.ajax_decline_applicant, name='ajax_decline_applicant'),
    path('ajax/hire_applicant/', views.ajax_hire_applicant, name='ajax_hire_applicant'),
    path('ajax/filter_postings/', views.ajax_filter_postings, name='ajax_filter_postings'),
    path('ajax/archive/', views.ajax_archive_postings, name='ajax_archive_postings'),
    path('ajax/add-to-posting/', views.ajax_add_to_posting, name='ajax_add_to_posting'),
]
