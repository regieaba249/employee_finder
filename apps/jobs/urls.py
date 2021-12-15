from django.urls import path
from . import views

app_name = 'apps.jobs'
urlpatterns = [
    path('board/', views.JobsBoardView.as_view(), name='jobs-board'),
]
