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
import json
import logging
import base64
from main.utilities.file_translation import file_translation_handler
import os
from datetime import datetime


documents_repo = r"documents_repo"

@login_required(login_url='users:login')
def Translation(request):
    if request.method == 'GET':
        allowed_langs = request.user.allowed_langs.values_list('code', flat=True)
        return render(request, 'main/translation.html', {"mode": "user", "source_lang": "en", "target_lang": "fa",
                                                         "main_page": True, "allowed_langs": allowed_langs})

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

        # Ensure user has permission for selected languages
        user_allowed_langs = request.user.allowed_langs.values_list('code', flat=True)
        if source_lang not in user_allowed_langs or target_lang not in user_allowed_langs:
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
def users_table(request,):
    # Fetch all users
    users = User.objects.all() # Assuming UserProfile is related to User
    # users = list(User.objects.all()) * 100

    # Pass users to the template
    return render(request, 'main/users_table.html', {
        'users': users,
    })


@admins_only
def edit_user(request, username):
    user = get_object_or_404(User, username=username)
    admin_group, created = Group.objects.get_or_create(name="Admin")
    user_level = "admin" if (user.groups.filter(name="Admin").exists() or user.is_superuser) else "regular"
    languages = Language.objects.all()

    if request.method == "POST":
        if "new_password" in request.POST:  # Password Change
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            if new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
            else:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password updated successfully.")
        
        else:  # Edit User Info
            user.username = request.POST["username"]
            user.first_name = request.POST.get("firstname", "")
            user.last_name = request.POST.get("lastname", "")
            user.email = request.POST.get("email", "")
            user.phone = request.POST.get("phone", "")
            selected_languages = request.POST.getlist("allowed_langs")
            user.allowed_langs.set(Language.objects.filter(code__in=selected_languages))
            user_level = request.POST.get("user_level", "regular")
            if user_level == "admin":
                user.groups.add(admin_group)
            else:
                user.groups.remove(admin_group)
            user.save()
            messages.success(request, "User updated successfully.")
        
        return redirect("main:edit_user", username=user.username)

    return render(request, "main/edit_user.html", {"user": user, "user_level": user_level, "languages": languages})


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
            email=email if email else None,
            phone=phone if phone else None,
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