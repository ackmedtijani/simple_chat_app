import json
from channels.db import database_sync_to_async

from channels.generic.websocket import AsyncWebsocketConsumer

from datetime import datetime , timedelta

from .models import Room , Message
from account.models import Token


def serialize_model_instance(model_instance):
    return {
        'id': model_instance.id,
        "body" : model_instance.body,
        'name': model_instance.sent_by.email,
        "created_at" : str(model_instance.created_at),
        "delivered" : model_instance.delivered,
        "read" : model_instance.seen,

        # Add more fields as needed
    }

class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def check_obj(self):
        try: 
            self.room = Room.objects.get(id = self.room_name)
            user = Token.objects.get(token = self.user_token).user

            if not self.room.participitants.filter(id=user.id).exists():
                self.room.participitants.add(user)

            self.scope["user"] = user

            messages = Message.objects.filter(room = self.room)

            if messages:
                return {"data" : [serialize_model_instance(obj) for obj in messages ]}
            
            return {"okay" : "User not part of the room"}

        except Room.DoesNotExist:
            return {"error" : "Room does not exist"}

        except Token.DoesNotExist:
             return {"error" : "Unauthenticated user"}


    async def connect(self):

        print(self.channel_name)

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user_token = self.scope["url_route"]["kwargs"]["api_key"]


        await self.channel_layer.group_add(self.room_group_name, self.channel_name)


        vae = await self.check_obj()
        value = vae.get("error")
        val = vae.get("data")

        if value:
            self.send(text_data = json.dumps({"error" : value}))
            await self.accept()
            self.disconnect()
        
        elif val:
            print("dadfad" , val)
            self.send(text_data = json.dumps({"data" : val}))
            await self.accept()
        # Join room group
        

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    
    @database_sync_to_async
    def get_message(self, message_id):
        message = Room.objects.get(pk = message_id)
        return message

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        mess = text_data_json["message"]
        
        message = await self.save_message(mess)

        self.scope

        if message.seen:
            await self.send(text_data = json.dumps({"type": "read_receipt" , "action" : "read" , "message_id" : message.id , "message" : mess}))

        else:
            await self.send(text_data = json.dumps({"type" : "read_receipt" , "action" : "delivered" , "message_id" : message.id , "message" : mess}))

        await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message", "message": mess , "message_id" : message.id , "exclude" : self.channel_name }
            )

            # Set the message as read

        # Send message to room group

    @database_sync_to_async
    def save_message(self , message):
        # Check the state of the channel layer
        try:
            return Message.objects.create(body = message , sent_by=self.scope["user"] , room = self.room)
        
        except Room.DoesNotExist:
            return Message.objects.create(body = message , sent_by=self.scope["user"] , room = self.room)
        except self.scope["user"].__class__.DoesNotExist:
            return Message.objects.create(body = message , sent_by=self.scope["user"] , room = self.room)

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        type_message = event["type"]
        exclude = event.get("exclude" , self.channel_name)
        message_id = event["message_id"]

        print("users" , self.scope["user"])
        print("1234124" , message)


        if exclude != self.channel_name:


        # Send message to WebSocket
            await self.send(text_data=json.dumps({"type" : "chat.message", "message": message , "message_id" : message_id}))

class ReadReceiptConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def check_obj(self):
        try: 
            self.room = Room.objects.get(id = self.room_name)
            user = Token.objects.get(token = self.user_token).user

            if not self.room.participitants.filter(id=user.id).exists():
                return {"error" : "User not part of the room"}

            self.scope["user"] = user
            return {"okay" : "User not part of the room"}

        except Room.DoesNotExist:
            return {"error" : "Room does not exist"}

        except Token.DoesNotExist:
            return {"error" : "Unauthenticated user"}


    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"read_receipt_{self.room_name}"
        self.user_token = self.user_token = self.scope["url_route"]["kwargs"]["api_key"]

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        value = await self.check_obj()
        value = value.get("error")

        if value:
            self.send(text_data = json.dumps({"error" : value}))
            self.disconnect()


    

   
        # Notify the sender that the message has been read
    @database_sync_to_async
    def mark_message_as_read(self, message_id):
        message = Message.objects.get(id = message_id)

        print("Message" , message)

        message.seen = True
        message.save()
        # Fetch the message from the database
        # Implement this method according to your model structure
        # Return the message object

    async def receive(self , text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json["message"]
        message_id =  text_data_json["message_id"]


        print("message" , message_id , self.scope["user"])

    

            # Set the message as read
        await self.mark_message_as_read(message_id)


        await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message", "action": "read" , "message_id" : message_id , "exclude" : self.channel_name}
                )
        
    async def chat_message(self, event):
        message = event["action"]
        message_id =  event["message_id"]
        exclude = event.get("exclude" , self.channel_name)

        print("23" ,message)

        if exclude != self.channel_name:

            print("454545" ,message)

        # Send message to WebSocket
            await self.send(text_data=json.dumps({"message_id": message_id , "action" : "read"}))

           
        

