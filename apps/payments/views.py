import stripe
from datetime import date
from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.http import (HttpResponseRedirect, JsonResponse)
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from django.views.generic.base import TemplateView

from .forms import PaymentForm
from .models import UserSubscription
from apps.users.models import CustomUser
from employee_finder.helpers import SUBSCRIPTION_TYPE


class SubscriptionPage(UserPassesTestMixin, TemplateView):
    template_name = 'cc_subscription_page.html'

    def test_func(self):
        user_id = self.kwargs.get('pk')
        user = CustomUser.objects.get(id=user_id)
        return not user.is_paid

    def get_context_data(self, *args, **kwargs):
        context = super(SubscriptionPage, self).get_context_data(*args, **kwargs)
        user_id = self.kwargs.get('pk')
        user = CustomUser.objects.get(id=user_id)
        context['user'] = user
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


def cc_charge(request, pk):
    user = CustomUser.objects.get(id=pk)
    amount = request.POST.get('amount')
    _type = request.POST.get('type')

    charge = stripe.Charge.create(
        amount=amount,
        currency='php',
        description='Premium Payment',
        receipt_email=user.email,
        source=request.POST.get('stripeToken'),
        api_key=settings.STRIPE_SECRET_KEY
    )
    if charge['captured']:
        user.is_paid = True
        user.save()

        months = {
            'monthly': 1,
            'semi': 6,
            'annually': 12,
        }

        subscription_data = {
            'user': user,
            'payment_type': _type,
            'price': f'{amount[:-2]}.{amount[-2:]}',
            'expiry_date': date.today() + relativedelta(months=months[_type]),
        }
        subscription = UserSubscription.objects.create(**subscription_data)
        subscription_type = dict(SUBSCRIPTION_TYPE)
        current_site = get_current_site(request)
        mail_subject = 'Activate your account'
        message = render_to_string('acc_active_paid_email.html', {
            'user': user,
            'subscription': subscription,
            'subscription_type': subscription_type[_type],
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': user.token,
        })
        to_email = user.email
        send_mail(
            mail_subject,
            message,
            settings.EMAIL_HOST_USER,
            [to_email],
            fail_silently=True,
        )

        messages.success(request, "Payment was Successful. Please validate via the email we sent to activate your account.")

    return HttpResponseRedirect(reverse_lazy('login'))
