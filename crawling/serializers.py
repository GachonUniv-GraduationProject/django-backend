from .models import data, keyword
from rest_framework import serializers


class dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = data
        fields = '__all__'


class keywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = keyword
        fields = '__all__'
