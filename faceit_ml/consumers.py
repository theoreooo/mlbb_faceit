# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)

class MatchmakingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = f"matchmaking_{self.scope['user'].id}"
        logger.info(f"Connecting user {self.scope['user'].id} to room {self.room_group_name}")

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        logger.info(f"Disconnecting user {self.scope['user'].id} from room {self.room_group_name}")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        logger.info(f"Received message: {data}")
        if data['type'] == 'match_found':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'match_found',
                    'message': data['message']
                }
            )

    async def match_found(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
