import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NikeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def nike_update(self, event):
        new_shoe_data = event['new_shoe_data']  # Assuming this is the new shoe data
        await self.send(text_data=json.dumps({
            'type': 'nike.update',
            'new_shoe': new_shoe_data,  # Include the new shoe data in the message
        }))