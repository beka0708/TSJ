from rest_framework import generics
from .models import Room, Message
from apps.chat.serializers import RoomSerializers, MessageSerializers
from django.shortcuts import render


def index(request):
    return render(request, 'chat.html')


class ChatListCreateView(generics.ListCreateAPIView):
    queryset = Room.objects.all().order_by('-created_at')
    serializer_class = RoomSerializers


class ChatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializers


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializers

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(room_id=chat_id).order_by('timestamp')

    def perform_create(self, serializer):
        chat_id = self.kwargs['chat_id']
        room = Room.objects.get(pk=chat_id)
        serializer.save(room=room, user=self.request.user)