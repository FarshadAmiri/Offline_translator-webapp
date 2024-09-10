from django.db import models
from users.models import User
from django.conf import settings


class TranslationTask(models.Model):
    task_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    source_language = models.CharField(max_length=255, null=False, default="English")
    target_language = models.CharField(max_length=255, null=False, default="Persian")
    source_text = models.TextField()
    translation = models.TextField(null=True)
    save_time = models.DateTimeField(auto_now_add=True)


class FileTranslationTask(models.Model):
    task_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    source_language = models.CharField(max_length=255, null=False, default="English")
    target_language = models.CharField(max_length=255, null=False, default="Persian")
    save_time = models.DateTimeField(auto_now_add=True)
    translated_percentage = models.IntegerField(null=True)