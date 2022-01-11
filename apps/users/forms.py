from apps.users.models import CustomUser
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string

from .tokens import account_activation_token

from .models import (
    Region,
    Province,
    Municipality,
    Barangay
)


class UserForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput
    )
    user_avatar = forms.ImageField(required=False)
    resume = forms.FileField(required=False)
    attachments = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False
    )

    class Meta:
        model = CustomUser

        fields = [
            'first_name',
            'last_name',
            'middle_name',
            'extension',
            'gender',
            'birthdate',
            'user_avatar',
            'area_code',
            'phone_number',
            'mobile_number',
            'address',
            'region',
            'province',
            'municipality',
            'barangay',
            'email',
            'headline',
            'overview',
            'user_type',
            'password1',
            'password2'
        ]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        MIN_LENGTH = 8
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        # At least MIN_LENGTH long
        if len(password1) < MIN_LENGTH:
            raise forms.ValidationError(f"The new password must be at least {MIN_LENGTH} characters long.")

        # At least one letter and one non-letter
        first_isalpha = password1[0].isalpha()
        if all(c.isalpha() == first_isalpha for c in password1):
            raise forms.ValidationError("The new password must contain at least one letter and at least one digit or" \
                                        " punctuation character.")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """user login form"""
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
        'required': True,
        'autofocus': True
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'required': True
    }))
    remember_me = forms.BooleanField(required=False)
