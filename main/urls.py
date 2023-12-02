from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'main'

urlpatterns = [
    path('', Translation, name='translation'),
    path('last_tasks', LastTasks, name='last_tasks'),
]