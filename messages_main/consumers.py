import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message


class DialogConsumer(WebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.dialog_group_name = 'dialog_%s' % self.chat_id

        # Присоедините потребителя к группе общения
        async_to_sync(self.channel_layer.group_add)(
            self.dialog_group_name,

        )

        self.accept()

    async def disconnect(self, close_code):
        # Отсоедините потребителя от группы общения
        async_to_sync(self.channel_layer.group_discard)(
            self.dialog_group_name,

        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Создайте сообщение в модели Message
        Message.objects.create(
            chat_id=self.chat_id,
            content=message
        )

        # Отправьте сообщение в группу общения
        async_to_sync(self.channel_layer.group_send)(
            self.dialog_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Отправьте сообщение на web-socket соединение
        self.send(text_data=json.dumps({
            'message': message
        }))
        
class ChatConsumer(WebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.chat_ids = self.scope['url_route']['kwargs']['chat_ids'].split(',')

        # Присоединение к группам чатов
        for chat_id in self.chat_ids:
            self.room_group_name = f'chat_{chat_id}'
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

        await self.accept()

    async def disconnect(self, close_code):
        for chat_id in self.chat_ids:
            self.room_group_name = f'chat_{chat_id}'
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        chat_ids = text_data_json['chat_ids'].split(',')

        # Отправка сообщения в указанные группы
        for chat_id in chat_ids:
            await self.channel_layer.group_send(
                f'chat_{chat_id}',
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': self.user.username,
                }
            )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Отправка сообщения в WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
