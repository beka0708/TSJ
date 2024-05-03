from django.contrib.auth import get_user_model
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from .models import DeviceToken

CustomUser = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    is_active = serializers.BooleanField(read_only=True)
    is_approved = serializers.CharField(read_only=True)
    verification_code = serializers.CharField(write_only=True)
    phone_number = PhoneNumberField()

    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'is_active', 'name', 'password', 'confirm_password', 'address', 'role',
                  'verification_code', 'is_approved')

    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')

        verification_code = validated_data.pop('verification_code')

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        user = CustomUser.objects.create_user(password=password, **validated_data)

        user.verification_code = verification_code
        return user


class DeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceToken
        fields = '__all__'
