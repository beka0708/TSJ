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


class NewsSerializer(serializers.ModelSerializer):
    views_count = serializers.SerializerMethodField()
    description = CKEditor5Field()

    class Meta:
        model = News
        fields = '__all__'

    def get_views_count(self, obj):
        return obj.views.count()


class VoteSerializer(serializers.ModelSerializer):
    views_count = serializers.SerializerMethodField()
    description = CKEditor5Field()
    room_url = serializers.SerializerMethodField()

    class Meta:
        model = Vote
        fields = "__all__"

    def get_views_count(self, obj):
        return obj.views.count()

    def get_room_url(self, obj):
        if obj.room:
            return obj.room.get_url()
        return None


class VoteResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteResult
        fields = '__all__'


class VoteViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteView
        fields = '__all__'


class RequestVoteSerializers(serializers.ModelSerializer):
    description = CKEditor5Field()

    class Meta:
        model = Request_Vote_News
        fields = "__all__"


class ApartmentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentHistory
        fields = '__all__'


