from rest_framework import generics, filters
from .models import Room, Message
from django_filters.rest_framework import DjangoFilterBackend
from apps.chat.serializers import RoomSerializers, MessageSerializers, RetrivRoomSerializer
from django.shortcuts import render, get_object_or_404


def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})


def chat_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    messages = Message.objects.filter(room=room).order_by('timestamp')
    return render(request, 'chat_room.html', {'room': room, 'messages': messages})


class ChatListCreateView(generics.ListCreateAPIView):
    queryset = Room.objects.all().order_by('-created_at')
    serializer_class = RoomSerializers
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    filterset_fields = ['is_archived', 'has_voting', 'is_discussion']


class ChatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializers

    def get_serializer_class(self):
        if self.request.method == 'GET' and self.kwargs.get('pk', None) is not None:
            return RetrivRoomSerializer
        return RoomSerializers


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializers

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(room_id=chat_id).order_by('timestamp')

    def perform_create(self, serializer):
        chat_id = self.kwargs['chat_id']
        room = Room.objects.get(pk=chat_id)
        serializer.save(room=room, user=self.request.user)
