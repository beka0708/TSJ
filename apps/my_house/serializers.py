from rest_framework import serializers
from .models import *
from apps.home.serializers import RequestVoteSerializers
from apps.userprofile.serializers import RequestSerializer


class DomKomSerializers(serializers.ModelSerializer):
    class Meta:
        model = DomKom
        fields = ('id', 'title', 'description', 'url', 'image', 'info')


class CameraSerializers(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ('id', 'url')


class ReceiptsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Receipts
        fields = ('id', 'title', 'cost', 'status', 'deadline')


class HelpInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = HelpInfo
        fields = ('id', 'tsj', 'title', 'url', 'number')
