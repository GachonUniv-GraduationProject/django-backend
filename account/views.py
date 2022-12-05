from knox.models import AuthToken
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from .models import *
from .serializers import CreateUserSerializer, UserSerializer, LoginUserSerializer, ProfileSerializer
from roadmap.models import skills

import socket
from _thread import *
import json

# HOST = '211.221.158.44'
# PORT = 48088
HOST = '127.0.0.1'
NLP_PORT = 9999
COMPANY_PORT = 9898

nlp_result = []
company_matching = []


# 소켓 통신을 위한 함수
def nlp_recv_data(client, data):
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


def company_recv_data(client, data):
    print(">> Connected with company")
    request_data = json.dumps(data)
    message = bytes(request_data, 'utf-8')
    client.send(message)
    while True:
        data = client.recv(10000)
        received_data = data.decode('utf-8')
        received_data = json.loads(received_data)
        if received_data != "":
            print("received_data :", received_data)
            company_matching.append(received_data)
            break


# Create your views here.
class RegistrationAPIView(APIView):
    def post(self, request):
        is_individual = request.GET.get('is_individual', True)
        if len(request.data["username"]) < 6 or len(request.data["password"]) < 4:
            body = {"message": "short field"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)

        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            AuthToken.objects.create(user)
            user_db = User.objects.get(username=request.data["username"])
            if is_individual == 'True':
                # experience 생성하는코드 추가해야함
                user_profile = Profile.objects.get(user_pk=user_db.pk)
                user_profile.phone = request.data['phone']
                user_profile.is_individual = is_individual
                user_profile.display_name = request.data['display_name']
                user_profile.save()
                return Response(serializer.data, status=201)
            else:
                company_profile = Company.objects.create(user=user_db,
                                                         user_pk=user_db.pk,
                                                         company_name=request.data['company_name'])
                company_profile.save()
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
        user_roadmap = Roadmap.objects.get(user_pk=user_pk)
        roadmap_field = user_roadmap.field_name
        roadmap_data = skills.objects.filter(field=roadmap_field)
        return_data = {"skill": []}
        completed = True
        locked = False
        for data in roadmap_data:
            temp_data = {}
            if data.base is None:
                temp_data["base"] = data.field

            else:
                temp_data["base"] = data.base.name
            temp_data["name"] = data.name
            temp_data["child"] = []
            temp_data["level"] = data.level
            for child in data.child.all():
                temp_data["child"].append(child.name)
            temp_data["completed"] = completed
            temp_data["locked"] = locked
            if data.name == user_roadmap.progress:
                completed = False
                locked = True
            return_data['skill'].append(temp_data)

        return Response(return_data, status=status.HTTP_200_OK)

    def post(self, request):
        user_pk = request.GET.get('user_pk', 1)
        print(user_pk)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, NLP_PORT))
        start_new_thread(nlp_recv_data, (client_socket, request.data))

        while len(nlp_result) == 0:
            continue
        return_data = nlp_result.pop()
        client_socket.close()
        return Response(return_data, status=status.HTTP_200_OK)

    def put(self, request):
        user_pk = request.GET.get('user_pk', 1)
        field = request.GET.get('field', "temp")
        name = request.data['name']
        user_roadmap = Roadmap.objects.get(user_pk=user_pk)
        user_roadmap.field_name = field
        if name == field:
            roadmap_skills = skills.objects.filter(field=field)
            children = roadmap_skills[0].child.all()
            child = children[0].child.all()[0].name
            user_roadmap.progress = child
            print(child)
        else:
            user_roadmap.progress = name
        # for child in children:
        #     print(child.name)
        user_roadmap.save()
        return_data = {"user_pk": user_pk, "field": field, "progress": user_roadmap.progress}
        return Response(return_data, status=status.HTTP_200_OK)


class ProfileCapabilityAPIView(APIView):
    def get_user(self, user_pk):
        return get_object_or_404(Profile, pk=user_pk - 2)

    def get(self, request):
        user_pk = request.GET.get('user_pk', 1)
        user_roadmap = Roadmap.objects.get(user_pk=user_pk)
        roadmap_field = user_roadmap.field_name
        cur_progress = user_roadmap.progress
        fields = request.data['fields']
        completed = []
        return_data = {"capability": []}
        main_field = skills.objects.filter(field=roadmap_field)
        locked = False
        for skill in main_field:
            if not locked:
                completed.append(skill.name)
            if skill.name == cur_progress:
                locked = True
        return_data['capability'].append({
            "name": roadmap_field,
            "total_curriculum": len(main_field),
            "completed": len(completed)})
        for field in fields:
            temp_field = skills.objects.filter(field=field)
            temp_completed = 0
            for skill in temp_field:
                if skill.name in completed:
                    temp_completed += 1
            return_data['capability'].append({
                "name": field,
                "total_curriculum": len(temp_field),
                "completed": temp_completed
            })

        return Response(return_data, status=status.HTTP_200_OK)


class CompanyAPIView(APIView):
    # json 파일 여는 함수
    def load_json(self):
        fields = {}
        with open('account/data/Backend_skill.json') as json_file:
            fields["Backend"] = json.load(json_file)["Backend"]

        with open('account/data/Frontend_skill.json') as json_file:
            fields["Frontend"] = json.load(json_file)["Frontend"]

        return fields

    def get(self, request):
        fields = self.load_json()
        # print(fields)
        field = request.data["data"]["company"]['field']
        company = Company.objects.get(user_pk=request.data["data"]["company"]['company_id'])
        users = Roadmap.objects.filter(field_name=field)
        roadmap_data = skills.objects.filter(field=field)
        to_socket = request.data

        to_socket['data']['user'] = []
        for user in users:
            print(user)
            temp_data = {'user_id': str(user.pk), 'field': user.field_name, 'skill': []}
            for data in roadmap_data:
                if data.name != user.progress:
                    if data.name in fields[field]["기술"] \
                            or data.name in fields[field]["프레임워크"] \
                            or data.name in fields[field]["기타"]:
                        temp_data['skill'].append(data.name)
                else:
                    break
            to_socket['data']['user'].append(temp_data)
        print(to_socket)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, COMPANY_PORT))
        start_new_thread(company_recv_data, (client_socket, to_socket))

        while len(company_matching) == 0:
            continue
        return_data = company_matching.pop()
        client_socket.close()
        return Response(return_data, status=status.HTTP_200_OK)


class MyPageAPIView(APIView):
    def get(self, request):
        user_pk = request.GET.get("user_pk", 1)
        user_experience = Experience.objects.filter(user_pk=user_pk)

        return Response({"user_pk": user_pk}, status=status.HTTP_200_OK)
