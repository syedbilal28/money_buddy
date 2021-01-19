import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer
from .models import Thread,ChatMessage
import channels.layers
from channels.generic.websocket import AsyncWebsocketConsumer
# from .serializer import ChatMessageSerializer

class ChatConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self,event):
        print("connected",event)
        self.channel_layer = channels.layers.get_channel_layer()
        print(self.scope['url_route']['kwargs'])
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']

        
        me = self.scope['user']
        print(me)
        thread_obj = await self.get_thread(self.thread_id)
        # print(thread_obj)
        # print(thread_id, me)
        self.thread_obj = thread_obj
        # print(thread_obj)
        chat_room = f"thread_{thread_obj.id}"
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            self.thread_id,
            self.channel_name
        )
        await self.accept()
    async def websocket_receive(self,event):
        print("received",event)
        front_text = event.get('text', None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
    #         
            msg = loaded_dict_data.get('message')

            print(msg)
            user = loaded_dict_data.get('username')
            # username=user.username
            myresponse = {
                'message': msg,
                'username': user
            }
            print("here")

            await self.channel_layer.group_send(
                self.thread_id,
                {
                    'type': 'chat_message',
                    'text': json.dumps(myresponse)
                }
            )
    

       


    async def chat_message(self, event):
        print("event",event)
        data=event['text']
        await self.send(text_data=json.dumps({
            'type': 'websocket.send',
            'text': data
        }))
    async def websocket_disconnect(self,event):
        print("disconnected",event)

    @database_sync_to_async
    def get_thread(self,roomname):
        return Thread.objects.get(pk=roomname)

    @database_sync_to_async
    def get_message(self,message,status):
        chatbox = ChatMessage.objects.get(pk=message)
        chatbox.status = status
        chatbox.save()
        print('success')

    @database_sync_to_async
    def get_chat_message(self, msg):
        thread_obj = self.thread_obj
        me = self.scope['user']
        return ChatMessage.objects.create(thread=thread_obj, user=me, message=msg)


    @database_sync_to_async
    def get_message_react(self, msg, chkstatus):
        print('////////////////////////')
        print(msg)
        chatbox = ChatMessage.objects.get(pk=msg - 1)
        if chkstatus == 'liked':
            chatbox.react_status = True
            chatbox.save()
        else:
            chatbox.react_status = False
            chatbox.save()
        print('success')

