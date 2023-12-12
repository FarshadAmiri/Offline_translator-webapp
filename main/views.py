from django.shortcuts import render, redirect, get_object_or_404
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
from django.contrib import auth, messages
from jdatetime import datetime as jdatetime, timedelta
from main.utilities.argos import translate_en_fa, translate_fa_en
from main.utilities.lang import detect_language
from main.utilities.encryption import *
# from datetime import datetime, timedelta
from .models import *
import logging
import base64


@login_required(login_url='users:login')
def Translation(request):
    if request.method == 'GET':
        return render(request, 'main/translation-Eng_default.html', {"eng_source": True,})
    
    elif (request.method == 'POST') and "translate-btn" in request.POST:
        source_lang = request.POST.get('btnradio_left')
        print(f"\nsource_lang: {source_lang}\n")
        target_lang = 'Persian' if source_lang == 'English' else 'English'
        encoded_text = request.POST.get('encodedText')
        encrypted_aes_key = request.POST.get('encryptedAESKey')
        print(f"\nencoded_text from client:\n{encoded_text}\n")
        print(f"\nencrypted_aes_key from client:\n{encrypted_aes_key}\n")
        encoded_text = encoded_text.split("%NEW_CHUNCK%")
        print(f"\n\n\nlength of encoded_text: {len(encoded_text)}\n\n\n")
        source_text = decode_chuncks(encoded_text, source_lang, chunkded=True)
        print(f"\n\ndecrypted_text: {source_text}\n\n")
        # source_text = base64.b64decode(encoded_text).decode('utf-8')
        detected_lang = detect_language(source_text)

        if detected_lang not in [None, source_lang]:
            print(f"\n\n\ndetected_lang: {detected_lang}\n\n\n")
            detect_lang_fa = "فارسی" if detected_lang == "Persian" else "انگلیسی"
            target_lang_fa = "فارسی" if detect_lang_fa == "انگلیسی" else "انگلیسی"
            messages.info(request, f'زبان ورودی {detect_lang_fa} شناسایی شد، در صورتیکه شما زبان ورودی را {target_lang_fa} انتخاب کردید. ترجمه بر اساس زبان ورودی {detect_lang_fa} و زبان مقصد {target_lang_fa} انجام شد.')
            # messages.info(request, f"Detected language is {detected_lang}, and you probably chose wrong input language! Translation performed based on {detected_lang} input.")
            source_lang = detected_lang
            
        if source_lang == "English":
            translation = translate_en_fa(source_text)
        elif source_lang == "Persian":
            translation = translate_fa_en(source_text)

        if source_lang == "English":
            return render(request, 'main/translation-Eng_default.html', {'translation': translation, "source_text": source_text,})
        elif source_lang == "Persian":
            return render(request, 'main/translation-Per_default.html', {'translation': translation, "source_text": source_text,})
    
    elif (request.method == 'POST') and "save-btn" in request.POST:
        source_lang = request.POST.get('btnradio_left')
        target_lang = 'Persian' if source_lang == 'English' else 'English'
        source_text = request.POST.get('source_text')
        translation = request.POST.get('translation')
        if source_text.strip() != "" or translation.strip() != "" :
            task = TranslationTask.objects.create(user=request.user, source_text=source_text, translation=translation,
                                                source_language=source_lang, target_language=target_lang)
            task.save()
    
        if source_lang == "English":
            return render(request, 'main/translation-Eng_default.html', {'translation': translation, "source_text": source_text,})
        elif source_lang == "Persian":
            return render(request, 'main/translation-Per_default.html', {'translation': translation, "source_text": source_text,})


@login_required(login_url='users:login')
def SavedTable(request):
    if request.method == 'GET':
        user=request.user
        saved_tasks = TranslationTask.objects.filter(user=user).order_by('-save_time')
        n_total_saved = len(saved_tasks)
        paginator = Paginator(saved_tasks, 10)
        num_pages = paginator.num_pages
        page_number = request.GET.get('page')
        try:
            page_objects = paginator.get_page(page_number)  # returns the desired page object
        except PageNotAnInteger:   # if page_number is not an integer then assign the first page
            page_objects = paginator.page(1)
        except EmptyPage:    # if page is empty then return last page
            page_objects = paginator.page(paginator.num_pages)
        
        for obj in page_objects:
            save_time = jdatetime.fromgregorian(datetime=obj.save_time)
            save_time = save_time + timedelta(hours=3, minutes=30)
            save_time = save_time.strftime("%Y/%m/%d ‌‌ ‌ ‌ ‌  %H:%M")
            obj.save_time = save_time

        for idx, obj in enumerate(page_objects[::-1]):
            obj.number = idx + 1

        context={'page_objects': page_objects, "n_total_saved": n_total_saved, "num_pages": num_pages, "user": user}
        return render(request, 'main/saved_table.html', context)
    

@login_required(login_url='users:login')
def EditText(request, task_id):
    if request.method == 'GET':
        user = request.user
        task = get_object_or_404(TranslationTask, user=user, task_id=task_id)
        source_text = task.source_text
        translation = task.translation
        source_lang = task.source_language
        target_lang = task.target_language

        if source_lang == "English":
            return render(request, 'main/translation-Eng_default.html', {'translation': translation, "source_text": source_text,
                                                                         "task_id": task_id, "edit_mode":True})
        elif source_lang == "Persian":
            return render(request, 'main/translation-Per_default.html', {'translation': translation, "source_text": source_text,
                                                                         "task_id": task_id, "edit_mode":True})
        
    elif (request.method == 'POST') and "translate-btn" in request.POST:
        source_lang = request.POST.get('btnradio_left')
        target_lang = 'Persian' if source_lang == 'English' else 'English'
        source_text = request.POST.get('source_text')
        detected_lang = detect_language(source_text)

        if detected_lang not in [None, source_lang]:
            print(f"\n\n\ndetected_lang: {detected_lang}\n\n\n")
            detect_lang_fa = "فارسی" if detected_lang == "Persian" else "انگلیسی"
            target_lang_fa = "فارسی" if detect_lang_fa == "انگلیسی" else "انگلیسی"
            messages.info(request, f'زبان ورودی {detect_lang_fa} شناسایی شد، در صورتیکه شما زبان ورودی را {target_lang_fa} انتخاب کردید. ترجمه بر اساس زبان ورودی {detect_lang_fa} و زبان مقصد {target_lang_fa} انجام شد.')
            source_lang = detected_lang
            
        if source_lang == "English":
            translation = translate_en_fa(source_text)
        elif source_lang == "Persian":
            translation = translate_fa_en(source_text)

        if source_lang == "English":
            return render(request, 'main/translation-Eng_default.html', {'translation': translation, "source_text": source_text, "task_id": task_id, "edit_mode":True})
        elif source_lang == "Persian":
            return render(request, 'main/translation-Per_default.html', {'translation': translation, "source_text": source_text, "task_id": task_id, "edit_mode":True})
        

    elif (request.method == 'POST') and "edit-btn" in request.POST:

        source_lang = request.POST.get('btnradio_left')
        target_lang = 'Persian' if source_lang == 'English' else 'English'
        source_text = request.POST.get('source_text')
        
        source_lang = request.POST.get('btnradio_left')
        target_lang = 'Persian' if source_lang == 'English' else 'English'
        source_text = request.POST.get('source_text')
        translation = request.POST.get('translation')
        detected_lang = detect_language(source_text)

        if detected_lang not in [None, source_lang]:
            source_lang = detected_lang

        if source_text.strip() != "" or translation.strip() != "" :
            task = TranslationTask.objects.create(user=request.user, source_text=source_text, translation=translation,
                                                source_language=source_lang, target_language=target_lang)
            task.save()
        else:
            task = TranslationTask.objects.get(task_id=task_id)
            task.delete()

        return HttpResponseRedirect(reverse('main:saved_table',))
    

    elif (request.method == 'POST') and "remove-btn" in request.POST:
        task = TranslationTask.objects.get(task_id=task_id)
        task.delete()

        return HttpResponseRedirect(reverse('main:saved_table',))


def DeleteText(request, task_id):
    if request.method == 'GET':
        user = request.user
        task = get_object_or_404(TranslationTask, user=user, task_id=task_id)
        task.delete()
        return HttpResponseRedirect(reverse('main:saved_table',))