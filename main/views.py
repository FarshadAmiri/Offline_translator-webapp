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
from .decorators import admins_only
from main.utilities.argos import translate_en_fa, translate_fa_en
from main.utilities.lang import detect_language
from main.utilities.encryption import *
# from datetime import datetime, timedelta
from .models import *
from users.models import User
import logging
import base64


@login_required(login_url='users:login')
def Translation(request):
    if request.method == 'GET':
        return render(request, 'main/translation-Eng_default.html', {"eng_source": True,})
    
    elif (request.method == 'POST') and "translate-btn" in request.POST:
        source_lang = request.POST.get('btnradio_left')
        target_lang = 'Persian' if source_lang == 'English' else 'English'
        encoded_text = request.POST.get('encryptedText')
        encrypted_aes_key = request.POST.get('encryptedAesKey')
        aes_key = decrypt_aes_key(encrypted_aes_key)
        source_text = decrypt_AES_ECB(encoded_text, aes_key)
        detected_lang = detect_language(source_text)

        if detected_lang not in [None, source_lang]:
            # detect_lang_fa = "فارسی" if detected_lang == "Persian" else "انگلیسی"
            # target_lang_fa = "فارسی" if detect_lang_fa == "انگلیسی" else "انگلیسی"
            # messages.info(request, f'زبان ورودی {detect_lang_fa} شناسایی شد، در صورتیکه شما زبان ورودی را {target_lang_fa} انتخاب کردید. ترجمه بر اساس زبان ورودی {detect_lang_fa} و زبان مقصد {target_lang_fa} انجام شد.')
            messages.info(request, f"Detected language is {detected_lang}, and you probably chose wrong input language! Translation performed based on {detected_lang} input.")
            source_lang = detected_lang
            
        if source_lang == "English":
            translation = translate_en_fa(source_text)
        elif source_lang == "Persian":
            translation = translate_fa_en(source_text)

        encrypted_translation = encrypt_AES_ECB(translation, aes_key).decode('utf-8')
        encrypted_source_text = encrypt_AES_ECB(source_text, aes_key).decode('utf-8')

        if source_lang == "English":
            return render(request, 'main/translation-Eng_default.html', {'translation': encrypted_translation, "source_text": encrypted_source_text,
                                                                         })
        elif source_lang == "Persian":
            return render(request, 'main/translation-Per_default.html', {'translation': encrypted_translation, "source_text": encrypted_source_text,
                                                                         })
    
    elif (request.method == 'POST') and "save-btn" in request.POST:
        source_lang = request.POST.get('btnradio_left')
        target_lang = 'Persian' if source_lang == 'English' else 'English'
        encoded_text = request.POST.get('encryptedText')
        encoded_translation = request.POST.get('encryptedTranslation')
        encrypted_aes_key = request.POST.get('encryptedAesKey')
        aes_key = decrypt_aes_key(encrypted_aes_key)
        source_text = decrypt_AES_ECB(encoded_text, aes_key)
        translation = decrypt_AES_ECB(encoded_translation, aes_key)
        detected_lang = detect_language(source_text)
        
        if source_text.strip() != "" or translation.strip() != "" :
            task = TranslationTask.objects.create(user=request.user, source_text=source_text, translation=translation,
                                                source_language=source_lang, target_language=target_lang)
            task.save()

        encrypted_translation = encrypt_AES_ECB(translation, aes_key).decode('utf-8')
        encrypted_source_text = encrypt_AES_ECB(source_text, aes_key).decode('utf-8')

        if source_lang == "English":
            return render(request, 'main/translation-Eng_default.html', {'translation': encrypted_translation, "source_text": encrypted_source_text, "aes_key": aes_key})
        elif source_lang == "Persian":
            return render(request, 'main/translation-Per_default.html', {'translation': encrypted_translation, "source_text": encrypted_source_text, "aes_key": aes_key})


@login_required(login_url='users:login')
def SavedTable(request):
    if request.method == 'POST':
        if "removingTextID" in request.POST:
            removing_text_id = int(request.POST.get('removingTextID'))
            user = request.user
            task = get_object_or_404(TranslationTask, user=user, task_id=removing_text_id)
            task.delete()
        encrypted_aes_key = request.POST.get('encryptedAesKey')
        aes_key = decrypt_aes_key(encrypted_aes_key)
        user=request.user
        saved_tasks = TranslationTask.objects.filter(user=user).order_by('-save_time')
        n_total_saved = len(saved_tasks)
        encrypted_saved_tasks = saved_tasks
        for idx, task in enumerate(encrypted_saved_tasks):
            task.source_text = encrypt_AES_ECB(task.source_text, aes_key).decode('utf-8')
            task.translation = encrypt_AES_ECB(task.translation, aes_key).decode('utf-8')
            task.order = n_total_saved - idx
        del saved_tasks
        paginator = Paginator(encrypted_saved_tasks, 5)
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

        context={'page_objects': page_objects, "n_total_saved": n_total_saved, "num_pages": num_pages,
                 "pages_range": paginator.page_range,"user": user, "mode": "normal", }
        return render(request, 'main/saved_table.html', context)
    


@admins_only
def SupervisorAllSavedTable(request):
    print("111")
    if request.method == 'POST':
        if "removingTextID" in request.POST:
            removing_text_id = int(request.POST.get('removingTextID'))
            user = request.user
            task = get_object_or_404(TranslationTask, user=user, task_id=removing_text_id)
            task.delete()
        encrypted_aes_key = request.POST.get('encryptedAesKey')
        aes_key = decrypt_aes_key(encrypted_aes_key)
        user=request.user
        saved_tasks = TranslationTask.objects.all().order_by('-save_time')
        n_total_saved = len(saved_tasks)
        encrypted_saved_tasks = saved_tasks
        for idx, task in enumerate(encrypted_saved_tasks):
            task.source_text = encrypt_AES_ECB(task.source_text, aes_key).decode('utf-8')
            task.translation = encrypt_AES_ECB(task.translation, aes_key).decode('utf-8')
            task.order = n_total_saved - idx
        del saved_tasks
        paginator = Paginator(encrypted_saved_tasks, 5)
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

        users_list = User.objects.all()
        context={'page_objects': page_objects, "n_total_saved": n_total_saved, "num_pages": num_pages,
                 "pages_range": paginator.page_range,"user": user, "mode": "supervisor", "users_list": users_list }
        return render(request, 'main/saved_table.html', context)
    

@admins_only
def SupervisorTable(request):
    user=request.user
    encrypted_aes_key = request.POST.get('encryptedAesKey')
    aes_key = decrypt_aes_key(encrypted_aes_key)
    selected_username = request.POST.get("selected_username", None)
    selected_username = "all_users" if selected_username == None else selected_username
    print("\n\nselected_username: ", selected_username, "\n\n")
    if selected_username == "all_users":
        saved_tasks = TranslationTask.objects.all().order_by('-save_time')
    else:
        selected_user=User.objects.get(username=selected_username)
        saved_tasks = TranslationTask.objects.filter(user=selected_user).order_by('-save_time')
    n_total_saved = len(saved_tasks)
    encrypted_saved_tasks = saved_tasks
    for idx, task in enumerate(encrypted_saved_tasks):
        task.source_text = encrypt_AES_ECB(task.source_text, aes_key).decode('utf-8')
        task.translation = encrypt_AES_ECB(task.translation, aes_key).decode('utf-8')
        task.order = n_total_saved - idx
    del saved_tasks
    paginator = Paginator(encrypted_saved_tasks, 5)
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

    users_list = User.objects.all()
    context={'page_objects': page_objects, "n_total_saved": n_total_saved, "num_pages": num_pages, "selected_user": selected_username,
             "pages_range": paginator.page_range, "user": user, "mode": "supervisor", "users_list": users_list }
    return render(request, 'main/supervisor_table.html', context)
    

@login_required(login_url='users:login')
def EditText(request, task_id):
    if (request.method == 'POST') and "translate-btn" in request.POST: # Translation
        print("\n\n\nTranslation mode in edit page\n\n\n\n")
        source_lang = request.POST.get('btnradio_left')
        target_lang = 'Persian' if source_lang == 'English' else 'English'
        encrypted_aes_key = request.POST.get('encryptedAesKey')
        aes_key = decrypt_aes_key(encrypted_aes_key)
        encrypted_source_text = request.POST.get('encryptedText')
        source_text = decrypt_AES_ECB(encrypted_source_text, aes_key)
        detected_lang = detect_language(source_text)

        if detected_lang not in [None, source_lang]:
            # print(f"\n\n\ndetected_lang: {detected_lang}\n\n\n")
            # detect_lang_fa = "فارسی" if detected_lang == "Persian" else "انگلیسی"
            # target_lang_fa = "فارسی" if detect_lang_fa == "انگلیسی" else "انگلیسی"
            # messages.info(request, f'زبان ورودی {detect_lang_fa} شناسایی شد، در صورتیکه شما زبان ورودی را {target_lang_fa} انتخاب کردید. ترجمه بر اساس زبان ورودی {detect_lang_fa} و زبان مقصد {target_lang_fa} انجام شد.')
            messages.info(request, f"Detected language is {detected_lang}, and you probably chose wrong input language! Translation performed based on {detected_lang} input.")
            source_lang = detected_lang
            
        if source_lang == "English":
            translation = translate_en_fa(source_text)
        elif source_lang == "Persian":
            translation = translate_fa_en(source_text)

        encrypted_translation = encrypt_AES_ECB(translation, aes_key).decode('utf-8')
        encrypted_source_text = encrypt_AES_ECB(source_text, aes_key).decode('utf-8')

        if source_lang == "English":
            return render(request, 'main/translation-Eng_default.html', {'translation': encrypted_translation, "source_text": encrypted_source_text, "task_id": task_id, "edit_mode":True})
        elif source_lang == "Persian":
            return render(request, 'main/translation-Per_default.html', {'translation': encrypted_translation, "source_text": encrypted_source_text, "task_id": task_id, "edit_mode":True})
        

    elif (request.method == 'POST') and "edit-btn" in request.POST:  # Edit

        source_lang = request.POST.get('btnradio_left')
        target_lang = 'Persian' if source_lang == 'English' else 'English'
        encrypted_aes_key = request.POST.get('encryptedAesKey')
        aes_key = decrypt_aes_key(encrypted_aes_key)
        encrypted_source_text = request.POST.get('encryptedText')
        encrypted_translation = request.POST.get('encryptedTranslation')
        source_text = decrypt_AES_ECB(encrypted_source_text, aes_key)
        translation = decrypt_AES_ECB(encrypted_translation, aes_key)
        detected_lang = detect_language(source_text)

        if detected_lang not in [None, source_lang]:
            source_lang = detected_lang

        if source_text.strip() != "" or translation.strip() != "" :
            task = TranslationTask.objects.get(task_id=task_id)
            task.source_text = source_text
            task.translation = translation
            task.source_language = source_lang
            task.target_language = target_lang
            task.save()
            
            encrypted_translation = encrypt_AES_ECB(translation, aes_key).decode('utf-8')
            encrypted_source_text = encrypt_AES_ECB(source_text, aes_key).decode('utf-8')

            if source_lang == "English":
                return render(request, 'main/translation-Eng_default.html', {'translation': encrypted_translation, "source_text": encrypted_source_text, "task_id": task_id, "edit_mode":True})
            elif source_lang == "Persian":
                return render(request, 'main/translation-Per_default.html', {'translation': encrypted_translation, "source_text": encrypted_source_text, "task_id": task_id, "edit_mode":True})
        else:
            task = TranslationTask.objects.get(task_id=task_id)
            task.delete()
            return HttpResponseRedirect(reverse('main:saved_table',))
    

    elif (request.method == 'POST') and (('remove-btn' in request.POST) or ('back-btn' in request.POST)): # Remove text or back
        if "remove-btn" in request.POST:
            task = TranslationTask.objects.get(task_id=task_id)
            task.delete()
        encrypted_aes_key = request.POST.get('encryptedAesKey')
        aes_key = decrypt_aes_key(encrypted_aes_key)
        user=request.user
        saved_tasks = TranslationTask.objects.filter(user=user).order_by('-save_time')
        n_total_saved = len(saved_tasks)
        encrypted_saved_tasks = saved_tasks
        for idx, task in enumerate(encrypted_saved_tasks):
            task.source_text = encrypt_AES_ECB(task.source_text, aes_key).decode('utf-8')
            task.translation = encrypt_AES_ECB(task.translation, aes_key).decode('utf-8')
            task.order = n_total_saved - idx
        del saved_tasks
        paginator = Paginator(encrypted_saved_tasks, 5)
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
    
    else: # Show text
        user = request.user
        task = get_object_or_404(TranslationTask, user=user, task_id=task_id)
        source_text = task.source_text
        translation = task.translation
        source_lang = task.source_language
        target_lang = task.target_language

        encrypted_aes_key = request.POST.get('encryptedAesKey')
        aes_key = decrypt_aes_key(encrypted_aes_key)
        encrypted_translation = encrypt_AES_ECB(translation, aes_key).decode('utf-8')
        encrypted_source_text = encrypt_AES_ECB(source_text, aes_key).decode('utf-8')

        if source_lang == "English":
            return render(request, 'main/translation-Eng_default.html', {'translation': encrypted_translation, "source_text": encrypted_source_text,
                                                                         "task_id": task_id, "edit_mode":True})
        elif source_lang == "Persian":
            return render(request, 'main/translation-Per_default.html', {'translation': encrypted_translation, "source_text": encrypted_source_text,
                                                                         "task_id": task_id, "edit_mode":True})


def DeleteText(request, task_id):
    if request.method == 'POST':
        encrypted_aes_key = request.POST.get('encryptedAesKey')
        user = request.user
        task = get_object_or_404(TranslationTask, user=user, task_id=task_id)
        task.delete()
        return HttpResponseRedirect(reverse('main:saved_table',))