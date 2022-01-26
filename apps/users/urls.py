from django.urls import path, re_path
from . import views

app_name = 'apps.users'
urlpatterns = [
    path('board/', views.ApplicantBoardView.as_view(), name='user-board'),
    path('test/', views.test, name='test'),
    path('profile/edit/<int:pk>/', views.CustomUserUpdateView.as_view(), name='profile_edit'),
    path('profile/view/<int:pk>/', views.CustomUserView.as_view(), name='profile_view'),
    path('register/<str:_type>/', views.RegistrationView.as_view(), name='register'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('ajax/load-address-dropdown/', views.ajax_load_address_dropdown, name='ajax_load_address_dropdown'),
    path('ajax/add-employment-history/', views.ajax_add_employment_history, name='ajax_add_employment_history'),
    path('ajax/add-education/', views.ajax_add_education, name='ajax_add_education'),
    path('ajax/add-skill/', views.ajax_add_skill, name='ajax_add_skill'),
    path('ajax/add-project/', views.ajax_add_project, name='ajax_add_project'),
    path('ajax/delete-data/', views.ajax_delete_data, name='ajax_delete_data'),
    path('ajax/delete-attachment/', views.ajax_delete_attachment, name='ajax_delete_attachment'),
    path('ajax/check-email/', views.ajax_check_email, name='ajax_check_email'),
    path('ajax/check-password/', views.ajax_check_password, name='ajax_check_password'),
    path('logout/', views.Logout, name='logout'),
]
