from django.contrib import admin
from .models import (
    SubscriptionType,
    UserSubscription
)


# Register your models here.
@admin.register(SubscriptionType)
class SubscriptionType(admin.ModelAdmin):
    search_fields = ('__all__',)


# Register your models here.
@admin.register(UserSubscription)
class UserSubscription(admin.ModelAdmin):
    search_fields = ('__all__',)
