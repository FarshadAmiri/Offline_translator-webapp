from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(required=False, max_length=100)
    password = forms.CharField(required=False, max_length=100, widget=forms.PasswordInput)
    captcha = CaptchaField()