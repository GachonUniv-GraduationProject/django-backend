from knox.models import AuthToken
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from .models import *
from .serializers import CreateUserSerializer, UserSerializer, LoginUserSerializer, ProfileSerializer
from roadmap.models import skills, url

import socket
from _thread import *
import json

# NLP_HOST = "127.0.0.1"
# COMPANY_HOST = "127.0.0.1"
# NLP_PORT = 9999
# COMPANY_PORT = 9898
NLP_HOST = '211.221.158.44'
COMPANY_HOST = '127.0.0.1'
NLP_PORT = 48088
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

                user_profile = Profile.objects.get(user_pk=user_db.pk)
                user_profile.phone = request.data['phone']
                user_profile.is_individual = is_individual
                user_profile.display_name = request.data['display_name']
                user_profile.save()

                return Response(serializer.data, status=201)
            else:
                company_profile = Company.objects.create(user=user_db,
                                                         user_pk=user_db.pk,
                                                         company_name=request.data['display_name'])
                company_profile.save()
                return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        roadmap = Roadmap.objects.get(user_pk=user.pk)
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
                "field": roadmap.field_name,
                "open_to_company": True
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
        now_uncomplete = False

        for data in roadmap_data:
            temp_data = {}
            if data.base is None:
                temp_data["base"] = data.field
            else:
                temp_data["base"] = data.base.name
            temp_data["name"] = data.name
            temp_data["level"] = data.level
            temp_data["child"] = []
            for child in data.child.all():
                temp_data["child"].append(child.name)
            if data.name == user_roadmap.progress:
                now_uncomplete = True
                completed = False

            if now_uncomplete and data.level == 1:
                locked = True

            temp_data["completed"] = completed
            temp_data["locked"] = locked
            # if data.name == user_roadmap.progress:
            #     lock_level = data.level
            #     lock = True
            #     completed = False
            # if lock and data.level == 1:
            #     locked = True
            return_data['skill'].append(temp_data)

        return Response(return_data, status=status.HTTP_200_OK)

    def post(self, request):
        user_pk = request.GET.get('user_pk', 1)
        user_db = User.objects.get(pk=user_pk)
        print(user_pk)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((NLP_HOST, NLP_PORT))
        start_new_thread(nlp_recv_data, (client_socket, request.data))

        while len(nlp_result) == 0:
            continue
        return_data = nlp_result.pop()
        client_socket.close()
        if request.data["type"] == "NLP_POS_NEG":
            for data in return_data["classify"]:
                user_field = Field.objects.create(user=user_db, user_pk=user_pk)
                user_field.name = data['field']
                user_field.preference = data['value']
                user_field.save()
            print(return_data)
        else:
            for data in return_data["classify"]:
                user_experience = Experience.objects.create(user=user_db, user_pk=user_pk)
                user_experience.field = data['field']
                user_experience.detail = data['sentence']
                user_experience.save()
            print(return_data)
        return Response(return_data, status=status.HTTP_200_OK)

    def put(self, request):
        user_pk = request.GET.get('user_pk', 1)
        field = request.GET.get('field', "temp")
        name = request.data['name']
        user_roadmap = Roadmap.objects.get(user_pk=user_pk)
        user_roadmap.field_name = field
        roadmap_skills = skills.objects.filter(field=field)
        if name == "next_level":
            index = 0
            for skill in roadmap_skills:
                if skill.name == user_roadmap.progress:
                    user_roadmap.progress = roadmap_skills[index + 1].name
                    user_roadmap.save()
                    return Response({"name": user_roadmap.progress})
                index += 1
        else:
            if name == field:
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

    def post(self, request):
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

    def post(self, request):
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
            temp_data = {'user_id': str(user.user_pk), 'field': user.field_name, 'skill': []}
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
        client_socket.connect((COMPANY_HOST, COMPANY_PORT))
        start_new_thread(company_recv_data, (client_socket, to_socket))

        while len(company_matching) == 0:
            continue
        return_data = company_matching.pop()
        client_socket.close()
        for user in return_data["recommended_user"]:
            recommend_user = RecommendProfile.objects.create(
                company=company,
                user_pk=user["user_id"],
                match_ratio=user["match_ratio"])
            user_skill = ""
            for skill in user["skill"]:
                user_skill += skill + ","
            recommend_user.skills = user_skill
            recommend_user.save()
        return Response(return_data, status=status.HTTP_200_OK)


class MyPageAPIView(APIView):
    def get(self, request):
        user_pk = request.GET.get("user_pk", 1)
        return_data = {"experience": [], "preference": []}
        user_experience = Experience.objects.filter(user_pk=user_pk)
        user_preference = Field.objects.filter(user_pk=user_pk)
        for experience in user_experience:
            temp = {"field": experience.field, "detail": experience.detail}
            return_data["experience"].append(temp)
        for field in user_preference:
            temp = {"field": field.name, "preference": field.preference}
            return_data["preference"].append(temp)

        return Response(return_data, status=status.HTTP_200_OK)


class CompanyRecommendationAPIView(APIView):

    def get(self, request):
        company_id = request.GET.get("company_id")
        company = Company.objects.get(user_pk=company_id)
        recommend_users = RecommendProfile.objects.filter(company=company)
        return_data = {"recommended_user": []}
        for user in recommend_users:
            print(user.user_pk)
            temp_user = User.objects.get(pk=user.user_pk)
            temp_roadmap = Roadmap.objects.get(user_pk=user.user_pk)
            temp = {"user_id": user.pk,
                    "match_ratio": user.match_ratio,
                    "user_email": temp_user.email,
                    "field": temp_roadmap.field_name}
            return_data["recommended_user"].append(temp)
            user_skills = user.skills.split(",")
            user_skills.pop()
            temp["skill"] = user_skills
            print(user_skills)
        return Response(return_data, status=status.HTTP_200_OK)


class RoadmapGetURLAPIView(APIView):
    def get(self, request):
        skill = request.GET.get("name")
        field = request.GET.get("field")
        request_skill = skills.objects.get(name=skill, field=field)
        request_urls = url.objects.filter(skill=request_skill)
        return_data = {"urls": []}
        for url_ in request_urls:
            temp_data = {"name": url_.link_name, "link": url_.link}
            return_data["urls"].append(temp_data)
        return Response(return_data, status=status.HTTP_200_OK)
