from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib import auth, messages
from jdatetime import datetime as jdatetime, timedelta
from .decorators import admins_only
from main.utilities.argos import translate
from main.utilities.pre_post_text_processing import modify_translation, preprocess_text, analyse_text, postprocess_text
from main.utilities.lang import detect_language
from main.utilities.encryption import *
# from datetime import datetime, timedelta
from .models import *
from users.models import User, Language
from django.contrib.auth.models import Group
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import OuterRef, Subquery, Count
import json
import logging
import base64
from main.utilities.file_translation import file_translation_handler
import os
from datetime import datetime


documents_repo = r"documents_repo"
language_code2name = {"fa":"Persian", "en": "English", "ar": "Arabic","he": "Hebrew"}
language_name2code = {v: k for k, v in language_code2name.items()}

@login_required(login_url='users:login')
def Translation(request):
    global language_code2name
    if request.method == 'GET':
        all_langs = {"English", "Arabic", "Persian", "Hebrew"}
        allowed_langs = set(request.user.allowed_langs.values_list('code', flat=True))
        unallowed_langs = all_langs - allowed_langs
        allowed_langs, unallowed_langs = list(allowed_langs), list(unallowed_langs)
        priority_langs = {"English": 4, "Arabic":3, "Hebrew":2, "Persian": 1}
        modified_priority_langs = {k: v for k, v in priority_langs.items() if k not in unallowed_langs}

        if len(allowed_langs) == 0:
            checked_source_lang = None
            checked_target_lang = None
        elif len(allowed_langs) == 1:
            checked_source_lang = allowed_langs[0]
            checked_target_lang = allowed_langs[0]
        elif len(allowed_langs) >= 2:
            checked_source_lang, checked_target_lang = sorted(modified_priority_langs, key=lambda x: modified_priority_langs[x], reverse=True)[:2]
            if "Persian" in allowed_langs:
                checked_target_lang = "Persian" 
        
        checked_source_lang = language_name2code[checked_source_lang]
        checked_target_lang = language_name2code[checked_target_lang]
        allowed_langs = [language_name2code[i] for i in allowed_langs]
        unallowed_langs = [language_name2code[i] for i in unallowed_langs]

        return render(request, 'main/translation.html', {"mode": "user", "source_lang": checked_source_lang, "target_lang": checked_target_lang, "main_page": True,
                                                          "allowed_langs": allowed_langs, "unallowed_langs": unallowed_langs, 
                                                          "checked_source_lang": checked_source_lang, "checked_target_lang": checked_target_lang})

    # elif (request.method == 'POST') and "translate-btn" in request.POST:
    #     source_lang = request.POST.get('source_lang')
    #     target_lang = request.POST.get('target_lang')
    #     encoded_text = request.POST.get('encryptedText')
    #     encrypted_aes_key = request.POST.get('encryptedAesKey')

    #     aes_key = decrypt_aes_key(encrypted_aes_key)
    #     source_text = decrypt_AES_ECB(encoded_text, aes_key)

    #     source_text_preprocessed = preprocess_text(source_text)
    #     source_text_analysis = analyse_text(source_text)
    #     translation = translate(source_text_preprocessed, source_lang, target_lang)
    #     translation = postprocess_text(translation, source_text_analysis)

    #     encrypted_translation = encrypt_AES_ECB(translation, aes_key).decode('utf-8')
    #     encrypted_source_text = encrypt_AES_ECB(source_text, aes_key).decode('utf-8')

    #     # Check if the request is AJAX
    #     if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    #         return JsonResponse({
    #             'translation': encrypted_translation,
    #             'source_text': encrypted_source_text,
    #             'source_lang': source_lang,
    #             'target_lang': target_lang,
    #         })
    #     else:
    #         return render(request, 'main/translation.html', {
    #             'translation': encrypted_translation,
    #             'source_text': encrypted_source_text,
    #             'mode': "user",
    #             'source_lang': source_lang,
    #             'target_lang': target_lang,
    #             'main_page': True,
    #         })

    elif request.method == 'POST' and "translate-btn" in request.POST:
        source_lang = request.POST.get('source_lang')
        target_lang = request.POST.get('target_lang')
        source_lang_name, target_lang_name = language_code2name[source_lang], language_code2name[target_lang]

        # Ensure user has permission for selected languages
        user_allowed_langs = request.user.allowed_langs.values_list('code', flat=True)
        if source_lang_name not in user_allowed_langs or target_lang_name not in user_allowed_langs:
            return JsonResponse({'error': 'You are not allowed to use these languages.'}, status=403)

        # Continue translation if languages are allowed
        encoded_text = request.POST.get('encryptedText')
        encrypted_aes_key = request.POST.get('encryptedAesKey')

        aes_key = decrypt_aes_key(encrypted_aes_key)
        source_text = decrypt_AES_ECB(encoded_text, aes_key)

        source_text_preprocessed = preprocess_text(source_text)
        source_text_analysis = analyse_text(source_text)
        translation = translate(source_text_preprocessed, source_lang, target_lang)
        translation = postprocess_text(translation, source_text_analysis)

        encrypted_translation = encrypt_AES_ECB(translation, aes_key).decode('utf-8')
        encrypted_source_text = encrypt_AES_ECB(source_text, aes_key).decode('utf-8')

        return JsonResponse({
            'translation': encrypted_translation,
            'source_text': encrypted_source_text,
            'source_lang': source_lang,
            'target_lang': target_lang,
        })

        
    elif (request.method == 'POST') and "save-btn" in request.POST:
        source_lang = request.POST.get('source_lang')
        target_lang = request.POST.get('target_lang')
        encoded_text = request.POST.get('encryptedText')
        encoded_translation = request.POST.get('encryptedTranslation')
        encrypted_aes_key = request.POST.get('encryptedAesKey')
        aes_key = decrypt_aes_key(encrypted_aes_key)
        source_text = decrypt_AES_ECB(encoded_text, aes_key)
        translation = decrypt_AES_ECB(encoded_translation, aes_key)
        
        if not ((source_text.strip() == "") and (translation.strip() == "")):
            task = TranslationTask.objects.create(
                user=request.user,
                source_text=source_text,
                translation=translation,
                source_language=source_lang,
                target_language=target_lang
            )
            task.save()

        encrypted_translation = encrypt_AES_ECB(translation, aes_key).decode('utf-8')
        encrypted_source_text = encrypt_AES_ECB(source_text, aes_key).decode('utf-8')

        # Check if the request is AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Translation saved successfully!',
                'translation': encrypted_translation,
                'source_text': encrypted_source_text,
            })
        else:
            return render(request, 'main/translation.html', {
                'translation': encrypted_translation,
                'source_text': encrypted_source_text,
                'mode': "user",
                'source_lang': source_lang,
                'target_lang': target_lang,
            })
                                                                     

    # elif (request.method == 'POST') and "save-btn" in request.POST:
    #     source_lang = request.POST.get('source_lang')
    #     target_lang = request.POST.get('target_lang')
    #     encoded_text = request.POST.get('encryptedText')
    #     encoded_translation = request.POST.get('encryptedTranslation')
    #     encrypted_aes_key = request.POST.get('encryptedAesKey')
    #     aes_key = decrypt_aes_key(encrypted_aes_key)
    #     source_text = decrypt_AES_ECB(encoded_text, aes_key)
    #     translation = decrypt_AES_ECB(encoded_translation, aes_key)
        
    #     if not ((source_text.strip() == "") and (translation.strip() == "")):
    #         task = TranslationTask.objects.create(user=request.user, source_text=source_text, translation=translation,
    #                                             source_language=source_lang, target_language=target_lang)
    #         task.save()

    #     encrypted_translation = encrypt_AES_ECB(translation, aes_key).decode('utf-8')
    #     encrypted_source_text = encrypt_AES_ECB(source_text, aes_key).decode('utf-8')

    #     return render(request, 'main/translation.html', {'translation': encrypted_translation, "source_text": encrypted_source_text,
    #                                                      "mode": "user", "source_lang": source_lang, "target_lang": target_lang, })


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
                 "pages_range": paginator.page_range,"user": user, "mode": "user", }
        return render(request, 'main/saved_table.html', context)
    

@admins_only
def SupervisorTable(request):
    user=request.user
    if request.method == 'POST':
        if "removingTextID" in request.POST:
            removing_text_id = int(request.POST.get('removingTextID'))
            print("\n\ndelete task id: ", removing_text_id, "\n\n")
            task = get_object_or_404(TranslationTask, task_id=removing_text_id)
            task.delete()
    encrypted_aes_key = request.POST.get('encryptedAesKey')
    aes_key = decrypt_aes_key(encrypted_aes_key)
    selected_username = request.POST.get("selected_username", None)
    selected_username = "all_users" if selected_username == None else selected_username
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
        mode = request.POST["mode"]
        source_lang = request.POST.get('source_lang')
        target_lang = request.POST.get('target_lang')
        encrypted_aes_key = request.POST.get('encryptedAesKey')
        aes_key = decrypt_aes_key(encrypted_aes_key)
        encrypted_source_text = request.POST.get('encryptedText')
        source_text = decrypt_AES_ECB(encrypted_source_text, aes_key)
        
        translation = translate(source_text, source_lang, target_lang)

        encrypted_translation = encrypt_AES_ECB(translation, aes_key).decode('utf-8')
        encrypted_source_text = encrypt_AES_ECB(source_text, aes_key).decode('utf-8')

        context = {'translation': encrypted_translation, "source_text": encrypted_source_text, "task_id": task_id, "edit_mode":True,
                   "mode": mode}
        
        return render(request, 'main/translation.html', {'translation': encrypted_translation, "source_text": encrypted_source_text,
                                                         "task_id": task_id, "edit_mode":True, "mode": mode, "source_lang": source_lang,
                                                         "target_lang": target_lang, })
        

    elif (request.method == 'POST') and "edit-btn" in request.POST:  # Edit
        mode = "user"
        source_lang = request.POST.get('source_lang')
        target_lang = request.POST.get('target_lang')
        encrypted_aes_key = request.POST.get('encryptedAesKey')
        aes_key = decrypt_aes_key(encrypted_aes_key)
        encrypted_source_text = request.POST.get('encryptedText')
        encrypted_translation = request.POST.get('encryptedTranslation')
        source_text = decrypt_AES_ECB(encrypted_source_text, aes_key)
        translation = decrypt_AES_ECB(encrypted_translation, aes_key)

        if not ((source_text.strip() == "") and (translation.strip() == "")):
            task = TranslationTask.objects.get(task_id=task_id)
            task.source_text = source_text
            task.translation = translation
            task.source_language = source_lang
            task.target_language = target_lang
            task.save()
            
            encrypted_translation = encrypt_AES_ECB(translation, aes_key).decode('utf-8')
            encrypted_source_text = encrypt_AES_ECB(source_text, aes_key).decode('utf-8')

            return render(request, 'main/translation.html', {'translation': encrypted_translation, "source_text": encrypted_source_text,
                                                    "task_id": task_id, "edit_mode":True, "mode": mode, "source_lang": source_lang,
                                                    "target_lang": target_lang, })
        else:
            task = TranslationTask.objects.get(task_id=task_id)
            task.delete()
            return HttpResponseRedirect(reverse('main:saved_table',))
    

    elif (request.method == 'POST') and (('remove-btn' in request.POST) or ('back-btn' in request.POST)): # Remove text or back
        if "remove-btn" in request.POST:
            task = TranslationTask.objects.get(task_id=task_id)
            task.delete()

        mode = request.POST['mode']
        if  mode == "supervisor":
            selected_username = request.POST["selected_user"] if "selected_user" in request.POST else "all_users"
        encrypted_aes_key = request.POST.get('encryptedAesKey')
        aes_key = decrypt_aes_key(encrypted_aes_key)
        user=request.user
        if mode == "supervisor":
            if selected_username == "all_users":
                saved_tasks = TranslationTask.objects.all().order_by('-save_time')
            else:
                saved_tasks = TranslationTask.objects.filter(user=selected_username).order_by('-save_time')
        else:
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
        if mode == "supervisor":
            users_list = User.objects.all()
            context={'page_objects': page_objects, "n_total_saved": n_total_saved, "num_pages": num_pages, "selected_user": selected_username,
                    "pages_range": paginator.page_range, "user": user, "mode": "supervisor", "users_list": users_list }
            return render(request, 'main/supervisor_table.html', context)
        context={'page_objects': page_objects, "n_total_saved": n_total_saved, "num_pages": num_pages, "pages_range": paginator.page_range, "user": user, "mode": "user",}
        return render(request, 'main/saved_table.html', context)
    
    else: # Show text
        mode = request.POST["mode"]
        user = request.user
        task = get_object_or_404(TranslationTask, task_id=task_id)
        source_text = task.source_text
        translation = task.translation
        source_lang = task.source_language
        target_lang = task.target_language

        encrypted_aes_key = request.POST.get('encryptedAesKey')
        aes_key = decrypt_aes_key(encrypted_aes_key)
        encrypted_translation = encrypt_AES_ECB(translation, aes_key).decode('utf-8')
        encrypted_source_text = encrypt_AES_ECB(source_text, aes_key).decode('utf-8')

        context = {'translation': encrypted_translation, "source_text": encrypted_source_text, "task_id": task_id,
                   "edit_mode":True, "mode": mode, "source_lang": source_lang, "target_lang": target_lang, }
        
        if (mode == "supervisor") and "selected_user" in request.POST:
            selected_user = request.POST["selected_user"]
            context["selected_user"] = selected_user
        
        return render(request, 'main/translation.html', context = context)
    


def DeleteText(request, task_id):
    if request.method == 'POST':
        encrypted_aes_key = request.POST.get('encryptedAesKey')
        user = request.user
        task = get_object_or_404(TranslationTask, user=user, task_id=task_id)
        task.delete()
        return HttpResponseRedirect(reverse('main:saved_table',))
    

# @csrf_exempt
# def file_translation(request):
#     if request.method == 'POST':
#         user = request.user
#         input_language = request.POST.get('input_language')
#         output_language = request.POST.get('output_language')
#         translation_task_id = request.POST.get('translation_task_id')
#         document = request.FILES.get('document')

#         if not document:
#             return JsonResponse({'success': False, 'error': 'No file uploaded.'})

#         # Input file naming
#         doc_name, doc_suffix = os.path.splitext(document.name)
#         formatted_datetime = datetime.now().strftime('%Y-%m-%d--%H-%M')
#         doc_save_name = f"{user.username}_{doc_name}_{formatted_datetime}{doc_suffix}"

#         # Save document to the specified repository
#         doc_path = os.path.join(documents_repo, doc_save_name)
#         doc_path = default_storage.get_available_name(doc_path)
#         default_storage.save(doc_path, ContentFile(document.read()))

#         # Define the output path for the translated file
#         output_path = os.path.splitext(doc_path)[0] + "_translation" + ".docx"

#         # Handle file translation (this function should perform the actual translation)
#         file_translation_handler(doc_path, output_path, input_language, output_language, translation_task_id)

#         # Ensure the file is properly handled and returned with correct headers
#         try:
#             with open(output_path, 'rb') as file:
#                 response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
#                 response['Content-Disposition'] = f'attachment; filename="{os.path.basename(output_path)}"'
#                 response['X-File-Name'] = os.path.basename(output_path)  # Adding file name to header
#                 return response
#         except FileNotFoundError:
#             return JsonResponse({'success': False, 'error': 'Translated file not found.'})
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)})

#     return JsonResponse({'success': False, 'error': 'Invalid request method.'})


@csrf_exempt
def file_translation(request):
    if request.method == 'POST':
        user = request.user
        input_language = request.POST.get('input_language')
        output_language = request.POST.get('output_language')
        translation_task_id = request.POST.get('translation_task_id')
        encrypted_data = request.POST.get('encryptedData')
        encrypted_aes_key = request.POST.get('encryptedAesKey')
        file_name = request.POST.get('fileInputName')
        aes_key = decrypt_aes_key(encrypted_aes_key)

        source_lang_name, target_lang_name = language_code2name[input_language], language_code2name[output_language]

        # Ensure user has permission for selected languages
        user_allowed_langs = request.user.allowed_langs.values_list('code', flat=True)
        if source_lang_name not in user_allowed_langs or target_lang_name not in user_allowed_langs:
            return JsonResponse({'error': 'You are not allowed to use these languages.'}, status=403)
    
        # Input file naming
        doc_name, doc_suffix = os.path.splitext(file_name)
        formatted_datetime = datetime.now().strftime('%Y-%m-%d--%H-%M')
        doc_save_name = f"{user.username}_{doc_name}_{formatted_datetime}{doc_suffix}"

        if encrypted_data:
            decrypted_data = decrypt_file_AES_ECB(encrypted_data, aes_key)

            # Create a Django file-like object from the decoded data
            document = ContentFile(decrypted_data, name=doc_save_name)
            print("\n\ndecryption done\n\n")


        # Save document to the specified repository
        doc_path = os.path.join(documents_repo, doc_save_name)
        doc_path = default_storage.get_available_name(doc_path)
        default_storage.save(doc_path, ContentFile(document.read()))

        # Define the output path for the translated file
        output_path = os.path.splitext(doc_path)[0] + "_translation" + ".docx"

        # Handle file translation (this function should perform the actual translation)
        file_translation_handler(doc_path, output_path, input_language, output_language, translation_task_id)

        try:
            with open(output_path, 'rb') as file:
                file_content = file.read()
                encrypted_file = encrypt_file_AES_ECB(file_content, aes_key)

                # response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response = HttpResponse(encrypted_file, content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(output_path)}"'
                response['X-File-Name'] = os.path.basename(output_path)  # Adding file name to header
                return response
        except FileNotFoundError:
            return JsonResponse({'success': False, 'error': 'Translated file not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


@csrf_exempt
def create_translation_task(request):
    if request.method == 'POST':
        input_language = request.POST.get('input_language')
        output_language = request.POST.get('output_language')

        if not input_language or not output_language:
            return JsonResponse({'success': False, 'error': 'Missing language parameters.'})

        user = request.user
        translation_task = FileTranslationTask.objects.create(
            user=user,
            source_language=input_language,
            target_language=output_language,
            progress="uploading"
        )
        return JsonResponse({'success': True, 'translation_task_id': translation_task.task_id})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


@csrf_exempt
def check_translation_progress(request):
    if request.method == 'GET':
        translation_task_id = request.GET.get('translation_task_id')
        
        if not translation_task_id:
            return JsonResponse({'success': False, 'error': 'Missing translation_task_id.'})

        try:
            task = FileTranslationTask.objects.get(task_id=translation_task_id)
            return JsonResponse({'success': True, 'progress': task.progress})

        except FileTranslationTask.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Translation task not found.'})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


@admins_only
def users_table(request):
    # Subqueries to count related records per user
    saved_texts_subquery = TranslationTask.objects.filter(user=OuterRef('pk')).order_by().values('user').annotate(count=Count('pk')).values('count')
    file_translations_subquery = FileTranslationTask.objects.filter(user=OuterRef('pk')).order_by().values('user').annotate(count=Count('pk')).values('count')

    # Fetch users along with related counts
    users = User.objects.annotate(
        num_saved_texts=Subquery(saved_texts_subquery, output_field=models.IntegerField()),
        num_file_translations=Subquery(file_translations_subquery, output_field=models.IntegerField())
    )
    
    # Convert created_at and last_login to Jalali datetime
    for user in users:
        if user.date_joined:
            date_joined_jalali = jdatetime.fromgregorian(date=user.date_joined)
            date_joined_jalali = date_joined_jalali + timedelta(hours=3, minutes=30)
            date_joined_jalali = date_joined_jalali.strftime("%Y/%m/%d ‌‌ ‌ ‌ ‌  %H:%M")
            user.date_joined_jalali = date_joined_jalali
        else:
            user.date_joined_jalali = None
        
        if user.last_login:
            last_login_jalali = jdatetime.fromgregorian(date=user.last_login)
            last_login_jalali = last_login_jalali + timedelta(hours=3, minutes=30)
            last_login_jalali = last_login_jalali.strftime("%Y/%m/%d ‌‌ ‌ ‌ ‌  %H:%M")
            user.last_login_jalali = last_login_jalali
        else:
            user.last_login_jalali = None

    return render(request, 'main/users_table.html', {
        'users': users,
    })

@admins_only
def edit_user(request, username):
    editing_user = get_object_or_404(User, username=username)
    admin_group, created = Group.objects.get_or_create(name="Admin")
    user_level = "admin" if (editing_user.groups.filter(name="Admin").exists() or editing_user.is_superuser) else "regular"
    languages = Language.objects.all()

    if request.method == "POST":
        if "new_password" in request.POST:  # Password Change
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            if new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
            else:
                editing_user.set_password(new_password)
                editing_user.save()
                messages.success(request, "Password updated successfully.")
        
        else:  # Edit User Info
            editing_user.username = request.POST["username"]
            editing_user.first_name = request.POST.get("firstname", "")
            editing_user.last_name = request.POST.get("lastname", "")
            editing_user.email = request.POST.get("email", "")
            editing_user.phone = request.POST.get("phone", "")
            selected_languages = request.POST.getlist("allowed_langs")
            editing_user.allowed_langs.set(Language.objects.filter(code__in=selected_languages))
            user_level = request.POST.get("user_level", "regular")
            if user_level == "admin":
                editing_user.groups.add(admin_group)
            else:
                editing_user.groups.remove(admin_group)
            editing_user.save()
            messages.success(request, "User updated successfully.")
        
        return redirect("main:edit_user", username=editing_user.username)

    return render(request, "main/edit_user.html", {"editing_user": editing_user, "user_level": user_level, "languages": languages})


@admins_only
def create_user(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        password = request.POST.get("password").strip()
        firstname = request.POST.get("firstname").strip().capitalize()
        lastname = request.POST.get("lastname").strip().capitalize()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        user_level = request.POST.get("user_level", "regular")
        allowed_langs = request.POST.getlist("allowed_langs")  # Get selected languages

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" already exists! Try another one')
            return render(request, "main/create_user.html")

        # Create new user
        user = User.objects.create_user(
            username=username,
            first_name = firstname if firstname else "",
            last_name = lastname if lastname else "",
            email=email if email else "",
            phone=phone if phone else "",
            password=password,
        )

        # Assign user level
        if user_level == "admin":
            supervisor_group, _ = Group.objects.get_or_create(name="Admin")
            user.groups.add(supervisor_group)

        # Save allowed languages (handling ManyToManyField)
        if allowed_langs:
            selected_languages = Language.objects.filter(code__in=allowed_langs)
            user.allowed_langs.set(selected_languages) 

        user.save()
        messages.success(request, f'User "{username}" created successfully!')
        return redirect("main:create_user")

    return render(request, "main/create_user.html")


@admins_only
def delete_user(request, username):
    user = get_object_or_404(User, username=username)
    
    if request.method == "POST":
        if user.is_superuser:
            messages.warning(request, "A Superuser cannot be deleted from here! Contact the management if you persist.")
            # return redirect("main:users_table")  # Redirect back to users list
            return redirect("main:edit_user", username=user.username)
        
        user.delete()
        messages.success(request, f'User "{username}" deleted successfully.')
        return redirect("main:users_table")  # Redirect back to users list
    
    return redirect("main:edit_user", username=username)
