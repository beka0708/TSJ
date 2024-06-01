import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Room, Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.room = await self.get_room(self.room_name)

        if self.room.is_archived:
            # Disconnect if the room is archived
            await self.close()
        else:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        # username = text_data_json.get('username')
        user = self.scope['user']
        room = await self.get_room(self.room_name)

        if not user.is_authenticated or room is None or not message:
            return

        if self.room.is_archived:
            # Do not process messages if the room is archived
            return

        # Save message to the database
        message_obj = await self.save_message(room, user, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': user.name if user.name else user.email,
                'timestamp': message_obj.timestamp.strftime('%m-%d %H:%M')
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        timestamp = event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'timestamp': timestamp,
        }))

    @database_sync_to_async
    def get_room(self, room_name):
        try:
            return Room.objects.get(title=room_name)
        except Room.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, room, user, message):
        return Message.objects.create(room=room, user=user, content=message)

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(pk=user_id)
