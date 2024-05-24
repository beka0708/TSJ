from django.contrib.auth import password_validation
from rest_framework import serializers
from .models import Profile, Request, ResidenceCertificate


class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name')
    email = serializers.EmailField(source='user.email')
    phone_number = serializers.CharField(source='user.phone_number')
    address = serializers.CharField(source='user.address')

    class Meta:
        model = Profile
        fields = ['id', 'name', 'email', 'phone_number', 'address', 'cover']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        user.name = user_data.get('name', user.name)
        user.email = user_data.get('email', user.email)
        user.phone_number = user_data.get('phone_number', user.phone_number)
        user.address = user_data.get('address', user.address)
        user.save()
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_new_password = serializers.CharField(required=True, write_only=True)

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


class ChangeSendPasswordSerializer(serializers.Serializer):
    verification_code = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({"confirm_new_password": "Новые пароли не совпадают."})
        return data


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('id', 'name_owner', 'tsj', 'number_flat', 'name', 'email', 'phone_number', 'created_date', 'status')


class ResidenceCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidenceCertificate
        fields = ['id', 'owner_surname', 'resident_surname', 'address', 'issue_date']
