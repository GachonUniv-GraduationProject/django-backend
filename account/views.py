from .serializers import UserSerializer
from .models import User, UserManager
from rest_framework import generics
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib import auth
import json


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def check_users(request):
    users = User.objects.all()
    for user in users:
        print(user)
        print(type(user))
        print(user.id)
    return HttpResponse("<h1>check log</h1>")


def logintest(request):
    data = json.loads(request.body)
    print(data['email'])
    print(auth.get_user(request))
    user = User.objects.get(nickname=data['nickname'])
    print(user)
    auth.login(request, user)
    print(auth.get_user(request))
    return HttpResponse("check log")


def signuptest(request):
    data = json.loads(request.body)
    print(data['nickname'])
    user = User.objects.create_user(data['email'],data['nickname'],data['name'],data['password'])
    print(user.password)
    get_user = User.objects.get(nickname=data['nickname'])
    print(get_user.password)
    return HttpResponse("check log")
