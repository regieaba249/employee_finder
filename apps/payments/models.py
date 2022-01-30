from django.db import models
from employee_finder.models import BaseModel
from employee_finder.helpers import (
    optional,
    SUBSCRIPTION_TYPE
)
from apps.users.models import CustomUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class SubscriptionType(BaseModel):
    name = models.CharField(max_length=5, blank=False)
    _type = models.CharField(
        choices=SUBSCRIPTION_TYPE,
        max_length=8,
        default='monthly',
        blank=False
    )
    price = models.FloatField(default=150, blank=False)

    def __str__(self):
        return f"{self.name} ({self.price})"


# Create your models here.
class UserSubscription(BaseModel):
    user = models.ForeignKey(
        CustomUser,
        related_name='subscriptions',
        on_delete=models.CASCADE,
        blank=False
    )
    is_current = models.BooleanField(_('is_current'), default=True)
    payment_type = models.CharField(
        choices=SUBSCRIPTION_TYPE,
        max_length=8,
        default='monthly',
        blank=False
    )
    price = models.FloatField(default=150, blank=False)
    paid_date = models.DateTimeField(auto_now_add=True, null=True)
    expiry_date = models.DateTimeField(blank=False)

    def __str__(self):
        return f"{self.user.email} ({self.payment_type})"
