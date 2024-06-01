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
    phone_number = PhoneNumberField()

    def validate_address(self, value):
        print("Validating address:", value)
        parts = value.split(',')
        if len(parts) != 4:
            raise serializers.ValidationError(
                "Адрес должен состоять из четырех частей:"
                " город, улица, номер дома, номер квартиры, разделенных запятыми.")
        try:
            house_number = int(parts[2].strip())  # Номер дома
            apartment_number = int(parts[3].strip())  # Номер квартиры
        except ValueError:
            raise serializers.ValidationError("Номер дома и номер квартиры должны быть числами.")

        return value

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "phone_number",
            "is_active",
            "name",
            "password",
            "confirm_password",
            "address",
            "role",
            "is_approved",
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        confirm_password = validated_data.pop("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop("verification_code", None)  # Удаление поля verification_code из ответа
        return data


class DeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceToken
        fields = "__all__"
