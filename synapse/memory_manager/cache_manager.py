import sys
from typing import Any, Optional
from connections.db import memcached_client

class CacheManager:
    def __init__(self, servers:list[str] = ["127.0.0.1"], capacity:int= 100000000, expire_time:int=3600):
        """
        Initialize the CacheManager with Memcached backend.
        
        :param servers: List of Memcached server addresses
        :capacity: Maximum size of the cache in bytes
        :param expire_time: Time in seconds after which an item should expire (0 means no expiration)
        """
        self.client = memcached_client()
        self.capacity = capacity
        self.expire_time = expire_time
        self.current_capacity = 0

    def get(self, key:str) -> Optional[Any]:
        """
        Retrieve an item from the cache.
        
        :param key: The key of the item to retrieve
        :return: The value associated with the key, or None if not found
        """
        try:
            return self.client.get(key)
        except pylibmc.Error:
            return None
        
    def put(self, key: str, value: bytes):
        value_size = sys.getsizeof(value)
        print(f"Storing key: {key}, value size: {value_size}")  # Debug print
        while self.current_capacity + value_size > self.capacity:
            self._evict_one()
        self.client.set(key, value, time=self.expire_time)
        self.current_capacity += value_size

    def evict(self, key:str):
        """
        Remove an item from the cache.
        
        :param key: The key of the item to remove
        """
        try:
            value = self.client.get(key)
            if value:
                self.current_capacity -= sys.getsizeof(value)
            self.client.delete(key)
        except pylibmc.Error:
            pass
    
    def _evict_one(self):
        """
        Evict one item from the cache when at capacity.
        This is a simplistic implementation and may not be the most efficient.
        """
        try:
            keys = self.client.get_stats()[0][1].get(b'curr_items', [])
            if keys:
                key_to_evict = keys[0]
                value = self.client.get(key_to_evict)
                if value:
                    self.current_capacity -= sys.getsizeof(value)
                self.client.delete(key_to_evict)
        except pylibmc.Error:
            pass