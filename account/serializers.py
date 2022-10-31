from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Profile


# class UserSerializer(serializers.ModelSerializer):
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             email=validated_data['email'],
#             nickname=validated_data['nickname'],
#             name=validated_data['name'],
#             password=validated_data['password']
#         )
#         return user
#
#     class Meta:
#         model = User
#         fields = ['nickname', 'email', 'name', 'password']

# 회원가입
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"], None, validated_data["password"]
        )
        return user


# 접속 유지중인지 확인
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


# 로그인
class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")


class ProfileSerializer(serializers.Serializer):
    class Meta:
        model = Profile
        fields = {"nickname", "phone"}

    def update(self, instance, validated_data):
        profile = Profile.objects.update()
