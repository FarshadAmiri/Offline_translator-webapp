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
from main.utilities.argos import translate_en_fa, translate_fa_en
# from datetime import datetime, timedelta
from .models import *
import logging


@login_required(login_url='users:login')
def Translation(request):
    if request.method == 'GET':
        return render(request, 'main/translation.html', {"eng_source": True,})
    
    elif request.method == 'POST':
        source_lang = request.POST.get('btnradio')
        print(f"\n\n\nsource_lang: {source_lang}\n\n\n")
        source_text = request.POST.get('source_text')
        if source_lang == "English":
            logging.info("English SELECTED")
            target_language = "Persian"
            translated_text = translate_en_fa(source_text)
        elif source_lang == "Persian":
            target_language = "English"
            translated_text = translate_fa_en(source_text)
        task = TranslationTask.objects.create(user=request.user, source_text=source_text, source_language=source_lang,
                                              target_language=target_language)
        task.save()
        # user_tasks = TranslationTask.objects.filter(user=request.user).order_by('-queried_at')[:50]
        # print("\n\n\nuser_tasks.first(): ", user_tasks.first() "\n\n\n")
        # TranslationTask.objects.filter(user=request.user, queried_at__lt=user_tasks.first().queried_at).delete()
        eng_source = True if source_lang == "English" else False
        return render(request, 'main/translation.html', {'translated_text': translated_text, "source_text": source_text,
                                                         "eng_source": eng_source,})
    

@login_required(login_url='users:login')
def LastTasks(request):
    if request.method == 'GET':
        user_tasks = TranslationTask.objects.filter(user=request.user).order_by('-queried_at')[:50]
        return render(request, 'main/last_tasks.html', {'user_tasks': user_tasks})