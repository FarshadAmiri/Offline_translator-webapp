from django.db import models
from django.contrib.auth.models import AbstractUser


class Language(models.Model):
    code = models.CharField(
        max_length=2, 
        unique=True, 
        choices=[("fa", "Farsi"), ("en", "English"), ("ar", "Arabic"), ("he", "Hebrew")]
    )

    def __str__(self):
        return self.get_code_display()


class User(AbstractUser):
    username = models.CharField(max_length=150, primary_key=True)
    email = models.EmailField(unique= False, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    allowed_langs = models.ManyToManyField(Language, blank=True)

    def __str__(self):
        return self.username

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    

