from rest_framework import serializers
from .models import *


class DomKomSerializers(serializers.ModelSerializer):
    class Meta:
        model = DomKom
        fields = ('id', 'title', 'description', 'url', 'image', 'info')


class YourFormsSerializers(serializers.ModelSerializer):
    class Meta:
        model = YourForms
        fields = ('id', 'user')


class CameraSerializers(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ('id', 'url')


class ReceiptsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Receipts
        fields = ('id', 'title', 'cost', 'status', 'deadline')


class HelpInfoSerializers(serializers.ModelSerializer):
    description = CKEditor5Field()

    class Meta:
        model = HelpInfo
        fields = ('id', 'tsj', 'title', 'url', 'number')
