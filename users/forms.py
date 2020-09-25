"""users app"""

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.db import models
from django import forms

from users.models import User


class RegistrationForm(forms.ModelForm):
    """Creating form for user registration"""
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]
        widgets = {
            "password": forms.PasswordInput(),
        }
        labels = {
            "email": "Email address",
        }
        help_texts = {
            'username': "letters and digits only",
        }

    def save(self, commit=True):
        self.instance.password = make_password(self.cleaned_data['password'])
        return super().save(self)

    def clean(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']
        if password != password_confirm:
            raise forms.ValidationError("passwords don't match")

        return self.cleaned_data

    def clean_username(self):
        username = self.data['username']
        if not username.isalpha():
            raise forms.ValidationError('use only numbers and letters for username')

        return username


class LoginForm(forms.Form):
    """Creating form for user login in"""
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput(),
    )

    def get_user(self, request):
        return authenticate(
            request,
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
        )


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField()

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]
