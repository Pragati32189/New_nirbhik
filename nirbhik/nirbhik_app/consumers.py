import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from .models import UserLocationRecordTable
from .serializers import UserLocationRecordSerializer

class UserLocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Check if the user is authenticated
        if self.scope["user"] is not AnonymousUser:
            await self.accept()  # Accept the WebSocket connection
            await self.send_user_locations()
        else:
            await self.close()

    async def disconnect(self, close_code):
        pass  # Handle disconnection if necessary

    async def receive(self, text_data):
        pass  # We won't be receiving any data from clients for now

    @database_sync_to_async
    def get_user_locations(self):
        user = self.scope["user"]
        locations = UserLocationRecordTable.objects.filter(user=user)
        serializer = UserLocationRecordSerializer(locations, many=True)
        return serializer.data

    async def send_user_locations(self):
        # Fetch all user location records
        user_locations = await self.get_user_locations()
        # Send the data to the WebSocket client
        await self.send(text_data=json.dumps({
            'locations': user_locations
        }))
