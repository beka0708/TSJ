from rest_framework import serializers

from .models import *


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


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = '__all__'


class DebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debt
        fields = '__all__'
