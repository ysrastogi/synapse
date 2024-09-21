
from connections.db import redis_client

class Publisher:
    def __init__(self, channel):
        self.channel = channel
        self.client = redis_client()
        self.subscribers = []

    def publish(self, message):
        self.client.publish(self.channel, message)

class Subscriber:
    def __init__(self, channel):
        self.channel = channel
        self.client = redis_client()
        self.pubsub = self.client.pubsub()
        self.pubsub.subscribe(self.channel)
    
    async def listen(self):
        await self.pubsub.subscribe(self.channel)
        async for message in self.pubsub.listen():
            if message['type'] == 'message':
                await self.callback(message['data'].decode('utf-8'))