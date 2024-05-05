from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name')
    email = serializers.EmailField(source='user.email')
    phone_number = serializers.CharField(source='user.phone_number')
    address = serializers.CharField(source='user.address')

    class Meta:
        model = Profile
        fields = ['name', 'email', 'phone_number', 'address', 'cover']

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
