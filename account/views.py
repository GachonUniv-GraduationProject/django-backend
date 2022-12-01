from knox.models import AuthToken
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from .models import Profile
from .serializers import CreateUserSerializer, UserSerializer, LoginUserSerializer, ProfileSerializer


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
            user_db = User.objects.get(username = request.data["username"])
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


# class ProfileUpdateAPI(generics.UpdateAPIView):
#     lookup_field = "user_pk"
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer


class ProfileDetailAPIView(APIView):
    def get_object(self, user_pk):
        return get_object_or_404(Profile, pk=user_pk-2)

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