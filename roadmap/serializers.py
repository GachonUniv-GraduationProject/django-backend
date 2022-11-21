from .models import url,skills
from rest_framework import serializers

class skillSerializer(serializers.ModelSerializer):
    class Meta:
        model = skills
        fields = '__all__'


class urlSerializer(serializers.ModelSerializer):
    class Meta:
        model = url
        fields = '__all__'

