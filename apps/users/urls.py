from django.urls import path, re_path
from . import views

app_name = 'apps.users'
urlpatterns = [
    path('test/', views.test, name='test'),
    path('profile/<int:pk>/', views.CustomUserUpdateView.as_view(), name='profile'),
    path('register/<str:_type>/', views.RegistrationView.as_view(), name='register'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('ajax/load-address-dropdown/', views.ajax_load_address_dropdown, name='ajax_load_address_dropdown'),
    path('ajax/add-employment-history/', views.ajax_add_employment_history, name='ajax_add_employment_history'),
    path('ajax/delete-data/', views.ajax_delete_data, name='ajax_delete_data'),
    path('logout/', views.Logout, name='logout'),
]
