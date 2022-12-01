from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Profile


# 회원가입
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"], validated_data["email"], validated_data["password"],
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


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

    def update(self, instance, validated_data):
        # user = self.context['request'].user
        # print(user)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.display_name = validated_data.get('display_name', instance.display_name)
        instance.is_individual = validated_data.get('is_individual', instance.is_individual)
        instance.save()

        return instance

    def create(self, validated_data):
        print(1)
        return Profile.objects.create(validated_data)
