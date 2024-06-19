from rest_framework import serializers
from .models import Room, Message
from apps.home.models import Vote


class VoteRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'title', 'created_date', 'deadline')


class RoomSerializers(serializers.ModelSerializer):
    vote = VoteRoomSerializer(read_only=True)

    class Meta:
        model = Room
        fields = ('title', 'description', 'created_at', 'vote', 'is_archived', 'has_voting', 'is_discussion')


class MessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
