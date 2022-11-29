from knox.models import AuthToken
from rest_framework import permissions, generics, status
from rest_framework.response import Response
import time

from .models import Profile
from .serializers import CreateUserSerializer, UserSerializer, LoginUserSerializer, ProfileSerializer


# Create your views here.
class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        if len(request.data["username"]) < 6 or len(request.data["password"]) < 4:
            body = {"message": "short field"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        time.sleep(2)
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


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


class ProfileUpdateAPI(generics.UpdateAPIView):
    lookup_field = "user_pk"
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # def put(self, request, *args, **kwargs):
    #     print(2)
    #     serializer = self.get_serializer(data = request.data)
    #     print(serializer.initial_data)
    #     print(self.request.user)
    #     print(3)
    #     serializer.is_valid(raise_exception=True)
    #
    #     profile = serializer.save()
    #     return Response(
    #         {
    #             "profile": ProfileSerializer(
    #                 profile, context=self.get_serializer_context()
    #             ).data,
    #         }
    #     )
