from .serializers import UserSerializer
from .models import User, UserManager, tech_stack
from rest_framework import generics
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib import auth
from django.views import View
import json


class IndexView(View):
    def get(self, request):
        cur_user = auth.get_user(request)
        return HttpResponse("<h1>cur user : " + str(cur_user.pk) + "</h1>")


class LoginView(View):
    def get(self, request):
        print(auth.get_user(request))
        cur_user = auth.get_user(request)
        return HttpResponse("<h1>cur user : " + cur_user.nickname + "</h1>")

    def post(self, request):
        data = json.loads(request.body)
        print(data['email'])
        print(auth.get_user(request))
        user = User.objects.get(nickname=data['nickname'])
        print(user)
        auth.login(request, user)
        print(auth.get_user(request))
        return HttpResponse("check log, new user has login")
    def delete(self, request):
        past_user = auth.get_user(request).nickname
        auth.logout(request)
        cur_user = auth.get_user(request)
        print(cur_user)

        return HttpResponse("<h1>" + past_user + " log out</h1>")


class SignupView(View):
    def get(self,request):
        return HttpResponse("<h1>use post request to signup</h1>")

    def post(self, request):
        data = json.loads(request.body)
        print(data['nickname'])
        if len(User.objects.filter(email=data['email'])) == 0:
            user = User.objects.create_user(data['email'], data['nickname'], data['name'], data['password'])
            print(user.password)
        else:
            print("duplicate user")
            return HttpResponse("duplicate user")
        get_user = User.objects.get(nickname=data['nickname'])
        print(get_user.password)
        return HttpResponse(get_user.email + " created")


class TechView(View):
    def get(self, request):
        cur_user = User.objects.get(pk=auth.get_user(request).pk)
        return HttpResponse(cur_user.tech_stacks)

    def post(self, request):
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
# class UserCreate(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# # 전체 유저 가져오는 함수
# def check_users(request):
#     users = User.objects.all()
#     for user in users:
#         print(user)
#         print(type(user))
#         print(user.id)
#     return HttpResponse("<h1>check log</h1>")
#
#
# # 이메일과 닉네임을 전달받고, 닉네임으로 유저 찾아서 로그인하는 함수
# def login_test(request):
#     data = json.loads(request.body)
#     print(data['email'])
#     print(auth.get_user(request))
#     user = User.objects.get(nickname=data['nickname'])
#     print(user)
#     auth.login(request, user)
#     print(auth.get_user(request))
#     return HttpResponse("check log, new user has login")
#
#
# # 회원가입 함수, 중복 유저 검증까지 어느정도 한다.
# def signup_test(request):
#     data = json.loads(request.body)
#     print(data['nickname'])
#     if len(User.objects.filter(email=data['email'])) == 0:
#         user = User.objects.create_user(data['email'], data['nickname'], data['name'], data['password'])
#         print(user.password)
#     else:
#         print("duplicate user")
#     get_user = User.objects.get(nickname=data['nickname'])
#     print(get_user.password)
#     return HttpResponse("check log")
#
#
# # 사용자 기술 스택 추가하는 함수
# def add_tech_stack(request):
#     data = json.loads(request.body)
#     print(auth.get_user(request))
#     techs = data['techs']
#     for tech in techs:
#         temp_tech = tech_stack.objects.filter(name=tech['name'])
#         if len(temp_tech) == 0:
#             stack_objects_create = tech_stack.objects.create(name=tech['name'])
#         else:
#             stack_objects_create = tech_stack.objects.get(name=tech['name'])
#
#         cur_user = User.objects.get(pk=auth.get_user(request).pk)
#         cur_user.tech_stacks.add(stack_objects_create)
#     return HttpResponse("check log")
#
#
# # 현재 유저를 확인하는 함수
# def user_check(request):
#     print(auth.get_user(request))
#     cur_user = auth.get_user(request)
#     return HttpResponse("<h1>cur user : " + cur_user.nickname + "</h1>")
#
#
# # 로그아웃하는 함수
# def logout(request):
#     past_user = auth.get_user(request).nickname
#     auth.logout(request)
#     cur_user = auth.get_user(request)
#     print(cur_user)
#
#     return HttpResponse("<h1>" + past_user + " log out</h1>")

# 리팩터링을 어떻게 진행해야될까
# https://eunjin3786.tistory.com/133
# 위 블로그 참고해서 만들면 될 것 같다.
