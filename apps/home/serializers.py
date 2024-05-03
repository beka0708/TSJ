from rest_framework import serializers
from .models import *


class HouseSerializers(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'


class FlatOwnerSerializers(serializers.ModelSerializer):
    class Meta:
        model = FlatOwner
        fields = '__all__'


class FlatTenantSerializers(serializers.ModelSerializer):
    class Meta:
        model = FlatTenant
        fields = '__all__'


class FlatSerializers(serializers.ModelSerializer):
    class Meta:
        model = Flat
        fields = '__all__'


class NewsOwnerSerializers(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class RequestSerializers(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'


class HelpInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = HelpInfo
        fields = '__all__'


class VoteNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteNew
        fields = '__all__'


class VotesSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Votes
        fields = ['user', 'vote']
#
#
# class VoteRecordSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VoteRecord
#         fields = '__all__'

# class VoteSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Vote
#         fields = '__all__'
