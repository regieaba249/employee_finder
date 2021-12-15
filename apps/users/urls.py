from django.urls import path, re_path
from . import views

app_name = 'apps.users'
urlpatterns = [
    path('test/', views.test, name='test'),
    path('profile/<int:pk>/', views.CustomUserUpdateView.as_view(), name='profile'),
    path('register/<str:_type>/', views.RegistrationView.as_view(), name='register'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('logout/', views.Logout, name='logout'),
]
