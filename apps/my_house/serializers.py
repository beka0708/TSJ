
from rest_framework import serializers

from .models import *


class DomKomSerializers(serializers.ModelSerializer):
    class Meta:
        model = DomKom
        fields = ('id', 'title', 'description', 'url', 'info')


class CameraSerializers(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ('id', 'url')


class HelpInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = HelpInfo
        fields = ('id', 'tsj', 'title', 'url', 'number')


class DebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debt
        fields = '__all__'


