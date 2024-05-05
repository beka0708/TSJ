from rest_framework import serializers
from .models import MyDetails, User, Request
from django.contrib.auth import password_validation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'address', 'phone_number']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = MyDetails
        fields = ['user', 'cover']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)  # Извлекаем данные пользователя, если они есть
        instance.cover = validated_data.get('cover', instance.cover)

        # Обновляем данные пользователя, если они предоставлены
        if user_data:
            user = instance.user
            user_serializer = UserSerializer(user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()  # Сохраняем изменения в модели User

        instance.save()  # Сохраняем изменения в модели MyDetails
        return instance

    # def update(self, instance, validated_data):
    #     instance.cover = validated_data.get('cover', instance.cover)
    #     instance.save()
    #     return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Старый пароль неверен.")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({"confirm_new_password": "Новые пароли не совпадают."})
        password_validation.validate_password(data['new_password'], self.context['request'].user)
        return data


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('id', 'name_owner', 'tsj', 'number_flat', 'name', 'email', 'number_phone', 'created_date', 'status')
