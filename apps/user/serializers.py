from rest_framework import serializers
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'email', 'name', 'password', 'confirm_password', 'address', 'role')

    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user

