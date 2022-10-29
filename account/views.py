from .serializers import UserSerializer
from .models import User, UserManager, tech_stack
# from rest_framework import
from django.contrib import auth
from django.views import View
import json

from django.contrib.auth import authenticate

# Create your views here.
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK


@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    data = json.loads(request.body)
    # email = request.data.get('email')
    # password = request.data.get('password')
    email = data['email']
    password = data['password']

    if email is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)

    # 여기서 authenticate로 유저 validate
    user = User.objects.get(email=email)

    # user = authenticate(email=email, password=password)

    if not user:
        return Response({'error': 'Invalid credentials'}, status=HTTP_404_NOT_FOUND)
    else:
        print(user.password)
        if user.password == password:
            auth.login(request,user)
            return Response({'login_user':user.email}, status=HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=HTTP_404_NOT_FOUND)


    # user 로 토큰 발행
    # token, _ = Token.objects.get_or_create(user=user)

    # return Response({'token': token.key}, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    data = json.loads(request.body)
    user = User.objects.create_user(data['email'], data['nickname'], data['name'], data['password'])
    if user:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


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
    def get(self, request):
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

# 리팩터링을 어떻게 진행해야될까
# https://eunjin3786.tistory.com/133
# 위 블로그 참고해서 만들면 될 것 같다.
