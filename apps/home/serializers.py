from rest_framework import serializers
from .models import *


class DeadLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeadLine
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HousePhoto
        fields = ('photo',)


class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseDeveloper
        fields = ('name', 'web_site')


class HouseSerializers(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)
    developer = DeveloperSerializer(read_only=True)

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
    tsj_id = serializers.IntegerField()

    class Meta:
        model = RequestVoteNews
        fields = ('title', 'description', 'deadline', 'tsj_id')

    def create(self, validated_data):
        user_id = self.context['user_id']
        request_vote = RequestVoteNews.objects.create(user_id=user_id, **validated_data)
        return request_vote


class ApartmentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentHistory
        fields = '__all__'


class TSJSerializer(serializers.ModelSerializer):
    class Meta:
        model = TSJ
        fields = '__all__'

