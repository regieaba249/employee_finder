from django.urls import path, re_path
from . import views

app_name = 'apps.companies'
urlpatterns = [
    path('profile/edit/<int:pk>/', views.CompanyUpdateView.as_view(), name='profile_edit'),
]
