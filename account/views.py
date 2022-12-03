from knox.models import AuthToken
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from .models import Profile, Roadmap
from .serializers import CreateUserSerializer, UserSerializer, LoginUserSerializer, ProfileSerializer
from roadmap.models import skills

import socket
from _thread import *
import json

# HOST = '211.221.158.44'
# PORT = 48088
HOST = '127.0.0.1'
PORT = 9999

nlp_result = []


# 소켓 통신을 위한 함수
def recv_data(client, data):
    print(">> Connected with nlp")
    request_data = json.dumps(data)
    message = bytes(request_data, 'utf-8')
    client.send(message)
    while True:
        data = client.recv(1024)
        received_data = data.decode('utf-8')
        received_data = json.loads(received_data)
        if received_data != "":
            print("received_data :", received_data)
            nlp_result.append(received_data)
            break


# Create your views here.
class RegistrationAPIView(APIView):
    def post(self, request):
        is_individual = request.GET.get('is_individual', True)
        print(request.GET.get('is_individual', False))
        if len(request.data["username"]) < 6 or len(request.data["password"]) < 4:
            body = {"message": "short field"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            AuthToken.objects.create(user)
            user_db = User.objects.get(username=request.data["username"])
            user_profile = Profile.objects.get(user_pk=user_db.pk)
            user_profile.phone = request.data['phone']
            user_profile.is_individual = is_individual
            user_profile.display_name = request.data['display_name']
            user_profile.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ProfileDetailAPIView(APIView):
    def get_object(self, user_pk):
        return get_object_or_404(Profile, pk=user_pk - 2)

    def get(self, request, user_pk):
        profile = self.get_object(user_pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, user_pk):
        profile = self.get_object(user_pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_pk):
        profile = self.get_object(user_pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileRoadmapAPIView(APIView):
    def get_user(self, user_pk):
        return get_object_or_404(Profile, pk=user_pk - 2)

    def get(self, request):
        user_pk = request.GET.get('user_pk', 1)

    def post(self, request):
        user_pk = request.GET.get('user_pk', 1)
        print(user_pk)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        start_new_thread(recv_data, (client_socket, request.data))

        while len(nlp_result) == 0:
            continue
        return_data = nlp_result.pop()
        client_socket.close()
        return Response(return_data, status=status.HTTP_200_OK)

    def put(self, request):
        user_pk = request.GET.get('user_pk', 1)
        field = request.GET.get('field', "temp")
        user_roadmap = Roadmap.objects.get(user_pk=user_pk)
        user_roadmap.field_name = field
        roadmap_skills = skills.objects.filter(field=field)
        children = roadmap_skills[0].child.all()
        child = children[0].child.all()[0].name
        user_roadmap.progress = child
        print(child)
        # for child in children:
        #     print(child.name)
        user_roadmap.save()
        return_data = {"user_pk": user_pk, "field": field, "progress": child}
        return Response(return_data, status=status.HTTP_200_OK)
