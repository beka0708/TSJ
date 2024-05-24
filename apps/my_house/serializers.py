from django.utils import timezone
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


class HelpInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = HelpInfo
        fields = ('id', 'tsj', 'title', 'url', 'number')


class DebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debt
        fields = '__all__'


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = ['id', 'name', 'amount', 'is_recurring', 'period']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'flat', 'payment_type', 'amount', 'status', 'created_at']


class CreatePaymentSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    flat_id = serializers.IntegerField()
    payment_type_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Payment
        fields = ['user_id', 'flat_id', 'payment_type_id', 'amount']

    def create(self, validated_data):
        user = User.objects.get(id=validated_data['user_id'])
        flat = Flat.objects.get(id=validated_data['flat_id'])
        payment_type = PaymentType.objects.get(id=validated_data['payment_type_id'])
        payment = Payment.objects.create(
            user=user,
            flat=flat,
            payment_type=payment_type,
            amount=validated_data['amount'],
            status='pending',
            created_at=timezone.now()
        )
        return payment