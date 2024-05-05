from rest_framework import serializers
from .models import (
    TSJ, House, FlatOwner, FlatTenant, Flat,
    News, HelpInfo, Vote
)


class TSJSerializer(serializers.ModelSerializer):
    class Meta:
        model = TSJ
        fields = ('id', 'name', 'house')


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ('id', 'name_block', 'address', 'geo_position', 'floors', 'entrances', 'flats_number')


class FlatOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlatOwner
        fields = ('id', 'tsj', 'user', 'flat')


class FlatTenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlatTenant
        fields = ('id', 'tsj', 'user', 'flat', 'owner')


class FlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flat
        fields = ('id', 'house', 'number')


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'tsj', 'type', 'title', 'description', 'link', 'created_date', 'update_date')


class HelpInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpInfo
        fields = ('id', 'tsj', 'title', 'url', 'number')


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'tsj', 'title', 'description', 'vote_type', 'users_votes', 'created_date', 'end_date')

