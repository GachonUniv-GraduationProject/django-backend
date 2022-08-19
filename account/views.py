from .serializers import UserSerializer
from .models import User
from rest_framework import generics
from django.shortcuts import render, HttpResponse


# 회원가입
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def check_user(request):
    users = User.objects.all()
    for user in users:
        print(user)
        print(type(user))
        print(user.id)
    return HttpResponse("<h1>check log</h1>")
