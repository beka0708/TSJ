from rest_framework import serializers
from .models import *


class HouseSerializers(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = "__all__"


class FlatOwnerSerializers(serializers.ModelSerializer):
    class Meta:
        model = FlatOwner
        fields = "__all__"


class FlatTenantSerializers(serializers.ModelSerializer):
    class Meta:
        model = FlatTenant
        fields = "__all__"


class FlatSerializers(serializers.ModelSerializer):
    class Meta:
        model = Flat
        fields = "__all__"


class NewsOwnerSerializers(serializers.ModelSerializer):
    description = CKEditor5Field()

    class Meta:
        model = News
        fields = "__all__"


class VoteSerializer(serializers.ModelSerializer):
    description = CKEditor5Field()

    class Meta:
        model = Vote
        fields = "__all__"


class VotesSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Votes
        fields = ["user", "vote"]


class RequestVoteSerializers(serializers.ModelSerializer):
    description = CKEditor5Field()

    class Meta:
        model = Request_Vote_News
        fields = "__all__"


