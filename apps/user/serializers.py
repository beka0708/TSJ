from django.contrib.auth import get_user_model
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from .models import DeviceToken
from apps.home.models import Flat, House, FlatOwner, TSJ

from django.db import transaction

CustomUser = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    phone_number = PhoneNumberField()
    tsj = serializers.IntegerField(write_only=True)

    def validate_address(self, value):
        print("Validating address:", value)
        parts = value.split(',')
        if len(parts) != 4:
            raise serializers.ValidationError(
                "Адрес должен состоять из четырех частей:"
                "город, улица, номер дома, номер квартиры, разделенных запятыми.")
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
            "name",
            "password",
            "confirm_password",
            "address",
            "role",
            "tsj"
        )

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop("password")
        confirm_password = validated_data.pop("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        # Извлечение адреса и других данных из validated_data
        address = validated_data.get("address")
        house_number = address.split(',')[2]
        flat_number = address.split(',')[3]

        # Получение tsj из validated_data
        tsj_id = validated_data.pop("tsj")

        # Создание пользователя
        user = CustomUser.objects.create_user(password=password, **validated_data)

        # Создание квартиры
        house = House.objects.filter(name_block=house_number).first()
        tsj = TSJ.objects.filter(id=tsj_id)
        if not tsj:
            raise serializers.ValidationError("TSJ with given id does not exist.")
        if not house:
            raise serializers.ValidationError("House with given number does not exist.")

        flat = Flat.objects.create(house_id=house.id, number=flat_number)

        # Создание владельца квартиры и привязка к пользователю и квартире
        FlatOwner.objects.create(user_id=user.id, flat_id=flat.id, tsj_id=tsj_id)

        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop("verification_code", None)  # Удаление поля verification_code из ответа
        return data


class DeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceToken
        fields = "__all__"


class PasswordResetRequestSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=4)
    new_password = serializers.CharField(write_only=True)
