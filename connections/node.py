import asyncio

from connections.db import redis_client
from connections.pubsub import Subscriber

class NodeRegistry:
    def __init__(self):
        self.nodes = {}
        self.client = redis_client()
    
    def register_node(self, node_id, channel, callback):
        if node_id not in self.nodes:
            self.nodes[node_id] = []
        
        subscriber = Subscriber(channel, callback)
        self.nodes[node_id].append(subscriber)
        asyncio.create_task(subscriber.listen())