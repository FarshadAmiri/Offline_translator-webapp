from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib import auth
from main.utilities.argos import translate_en_fa
# from datetime import datetime, timedelta
from .models import *


@login_required(login_url='users:login')
def Translation(request):
    if request.method == 'GET':
        return render(request, 'main/translation.html')
    
    elif request.method == 'POST':
        eng_text = request.POST.get('eng_text')
        task = TranslationTask.objects.create(user=request.user, source_text=eng_text, source_language="English", target_language="Persian")
        task.save()
        # user_tasks = TranslationTask.objects.filter(user=request.user).order_by('-queried_at')[:50]
        # print("\n\n\nuser_tasks.first(): ", user_tasks.first() "\n\n\n")
        # TranslationTask.objects.filter(user=request.user, queried_at__lt=user_tasks.first().queried_at).delete()
        translated_text = translate_en_fa(eng_text)
        return render(request, 'main/translation.html', {'translated_text': translated_text, "eng_text": eng_text})
    

@login_required(login_url='users:login')
def LastTasks(request):
    if request.method == 'GET':
        user_tasks = TranslationTask.objects.filter(user=request.user).order_by('-queried_at')[:50]
        return render(request, 'main/last_tasks.html', {'user_tasks': user_tasks})