from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse ,reverse_lazy
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import UpdateView, DetailView, DeleteView
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
# from rest_framework.views import APIView
# from rest_framework.generics import GenericAPIView
# from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
# from rest_framework.response import Response
from .models import *

def login_view(request, *kwargs):
    if request.method =='GET':
        return render(request, 'Login_page.html')
    elif request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('main:translation'))
        message = 'Invalid Credentials!'
        return render(request, 'Login_page.html', {'message':message})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('main:translation'))


def profile_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            # user_profile = get_object_or_404(Profile, username=request.user.username)
            return render (request, 'Profile_page.html', {'user': request.user
                                                              # ,'user_profile': user_profile
                                                              })
        return HttpResponse('You Must Log In First')