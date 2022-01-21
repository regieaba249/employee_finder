from django.urls import path, re_path
from . import views

app_name = 'apps.payments'
urlpatterns = [
    path('cc-charge/<int:pk>/', views.cc_charge, name='cc_charge'),
    path('cc-subscription-page/<int:pk>/', views.SubscriptionPage.as_view(), name='cc_subscription_page'),
]
