from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
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

    async def receive_json(self, content, **kwargs):
        message = content['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                # 'type': 'chat_message',
                'type': 'chat_message_with_end',
                'message': message
            }
        )
        await self.send_json({'message': message, 'is_group': False})

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send_json({'message': message})

    async def chat_message_with_end(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send_json({'message': message, 'is_group': True})


class DataServer(AsyncConsumer):
    async def summary(self, event):
        message = event['message']
        await self.channel_layer.group_send(
            'chat_summary',
            {
                'type': 'chat_message',
                'message': message
            }
        )
