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
    path('document_translation/', file_translation, name='document_translation'),
    path('create_translation_task/', create_translation_task, name='create_translation_task'),
    path('file_translation/', file_translation, name='file_translation'),
    path('check_translation_progress/', check_translation_progress, name='check_translation_progress'),
    path('users_table/', users_table, name='users_table'),
    path('edit-user/<str:username>/', edit_user, name='edit_user'),
    path('create-user/', create_user, name='create_user'),
    path('users/<str:username>/delete/', delete_user, name="delete_user"),

]