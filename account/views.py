from .serializers import UserSerializer
from .models import User, UserManager, tech_stack
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


def login_test(request):
    data = json.loads(request.body)
    print(data['email'])
    print(auth.get_user(request))
    user = User.objects.get(nickname=data['nickname'])
    print(user)
    auth.login(request, user)
    print(auth.get_user(request))
    return HttpResponse("check log")


def signup_test(request):
    data = json.loads(request.body)
    print(data['nickname'])
    if len(User.objects.filter(email=data['email'])) == 0:
        user = User.objects.create_user(data['email'],data['nickname'],data['name'],data['password'])
        print(user.password)
    else:
        print("duplicate user")
    get_user = User.objects.get(nickname=data['nickname'])
    print(get_user.password)
    return HttpResponse("check log")


def add_tech_stack(request):
    data = json.loads(request.body)
    print(auth.get_user(request))
    techs = data['techs']
    for tech in techs:
        temp_tech = tech_stack.objects.filter(name=tech['name'])
        if len(temp_tech) == 0:
            stack_objects_create = tech_stack.objects.create(name=tech['name'])
        else:
            stack_objects_create = tech_stack.objects.get(name=tech['name'])

        cur_user = User.objects.get(pk=auth.get_user(request).pk)
        cur_user.tech_stacks.add(stack_objects_create)
    return HttpResponse("check log")


# def user_check(request):
