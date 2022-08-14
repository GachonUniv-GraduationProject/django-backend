from rest_framework import serializers
from .models import Person


class BasePersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name', 'phone', 'addr','email')


class EmailPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'email')
