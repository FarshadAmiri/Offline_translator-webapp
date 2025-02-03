from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser']

    allowed_langs = forms.CharField(max_length=255, required=False)

    def save(self, commit=True):
        user = super().save(commit=commit)
        user_profile, created = User.objects.get_or_create(user=user)
        user_profile.allowed_langs = self.cleaned_data['allowed_langs']
        user_profile.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(required=False, max_length=100)
    password = forms.CharField(required=False, max_length=100, widget=forms.PasswordInput)
    captcha = CaptchaField()