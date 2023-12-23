from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'main'

urlpatterns = [
    path('', Translation, name='translation'),
    path('saved/', SavedTable, name='saved_table'),
    path('supervisor_table/', SupervisorTable, name='supervisor_table'),
    path('delete/?id=<int:task_id>/', DeleteText, name='delete_saved_text'),
    path('edit_text?<int:task_id>/', EditText, name='edit_saved_text'),
]