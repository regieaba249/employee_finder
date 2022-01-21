from django import forms


class PaymentForm(forms.Form):
    """user login form"""
    card_number = forms.CharField(required=True)
    exp_month = forms.IntegerField(required=True)
    exp_year = forms.IntegerField(required=True)
    cvc = forms.IntegerField(required=True)
